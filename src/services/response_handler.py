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
            return results.AboutMeUsernameResult(
                first_name=user_info["first_name"],
                last_name=user_info["last_name"],
                interests=[item["interest"] for item in user_info["interests"]],
                location=user_info["locations"][0]["location"],
                social_media_links=[app["site_url"] for app in user_info["apps"]]
            )

    return None


RESPONSE_HANDLERS: Dict[str, Callable] = {
    "about_me_find_account": about_me_email_handler,
    "about_me_username_lookup": about_me_profile_handler
}


def handle_response(response: models.HttpResponse) -> results.Result:
    handler = RESPONSE_HANDLERS[response.name]
    return handler(response)
