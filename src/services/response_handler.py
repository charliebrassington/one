import json

from src.domain import results, models
from typing import Callable, Dict


def about_me_email_handler(
    response: models.HttpResponse
) -> results.AboutMeEmailResult | None:
    if response.status_code == 200:
        return results.AboutMeEmailResult(
            **json.loads(response.content)
        )

    return None


def about_me_profile_handler(
    response: models.HttpResponse
) -> results.AboutMeUsernameResult | None:
    for script in response.soup.find_all("script"):
        script_text = script.text
        if "DOMAIN_NAME" in script_text:
            data = json.loads(script_text)
            user_info = data["page"]["user"]
            if user_info is None:
                return None

            return results.AboutMeUsernameResult(
                first_name=user_info["first_name"],
                last_name=user_info["last_name"],
                interests=[item["interest"] for item in user_info["interests"]],
                location=user_info["locations"][0]["location"],
                social_medias=[app["site_url"] for app in user_info["apps"]]
            )

    return None


def company_house_person_handler(
    response: models.HttpResponse
) -> results.CompanyHouseFullnameResult | None:
    officer_element = response.soup.find("li", {"class": "type-officer"})
    p_tag_elements = officer_element.find_all("p")

    birth_info = p_tag_elements[0].text.split()
    birth_year, birth_month = birth_info[-1], birth_info[-2]

    if len(birth_year) != 4:
        return None

    return results.CompanyHouseFullnameResult(
        fullname=officer_element.find("a", href=True).text,
        birth_year=birth_info[-1],
        birth_month=birth_info[-2],
        address=p_tag_elements[1].text
    )


def gravatar_profile_handler(
    response: models.HttpResponse
):
    if response.status_code == 404:
        return None

    data = json.loads(response.content)
    profile_dict = data["entry"][0]
    return results.GravatarEmailResult(
        social_medias=profile_dict["profileUrl"],
        username=profile_dict["preferredUsername"],
        photos=[photo["value"] for photo in profile_dict["photos"]]
    )


def discord_invite_handler(
    response: models.HttpResponse
):
    print(response.content)
    data = json.loads(response.content)
    if "inviter" not in data:
        return None

    inviter_data = data["inviter"]
    return results.DiscordInviteResult(
        discord_id=inviter_data["id"],
        discord_username=inviter_data["username"],
        photos=f"https://cdn.discordapp.com/avatars/{inviter_data['id']}/{inviter_data['avatar']}.png?size=1024"
    )


def plancke_profile_handler(
    response: models.HttpResponse
):
    soup = response.soup
    discord_username = None
    for script in soup.find_all("script"):
        if "social_DISCORD" in script.text:
            discord_username = script.text.split('Discord", "')[1].split('");')[0]

    return results.PlanckeProfile(
        discord_username=discord_username,
        social_medias=[
            link_element["href"]
            for link_element in soup.find_all("a", {"target": "_blank"}, href=True)
            if not link_element["href"].startswith("https://github.com")
        ]
    )


RESPONSE_HANDLERS: Dict[str, Callable] = {
    "about_me_find_account": about_me_email_handler,
    "about_me_username_lookup": about_me_profile_handler,
    "company_house_fullname_lookup": company_house_person_handler,
    "gravatar_email_lookup": gravatar_profile_handler,
    "discord_invite_code_lookup": discord_invite_handler,
    "plancke_minecraft_username_lookup": plancke_profile_handler
}


def handle_response(response: models.HttpResponse | None) -> results.Result | None:
    if response is None:
        return None

    handler = RESPONSE_HANDLERS[response.name]
    return handler(response)
