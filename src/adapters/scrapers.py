import aiohttp
import json
import hashlib

from typing import Type, Coroutine, Any
from src.domain import models


class Scraper:
    information: models.ScraperMetadata

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def make_request(
        self,
        method: str,
        request_name: str,
        **kwargs
    ) -> models.HttpResponse:
        """
        Making requests with the session.

        :param method:
        :param request_name:
        :param kwargs:
        :return: models.HttpResponse
        """
        print(f"Sent request {request_name}")
        async with getattr(self.session, method)(**kwargs) as response:
            content = await response.text()
            print(f"Finished request {request_name}")
            return models.HttpResponse(
                name=request_name,
                content=content,
                status_code=response.status
            )


class AboutMeScraper(Scraper):
    information = models.ScraperMetadata(
        name="About me scraper",
        main_url="https://about.me/",
        functions={
            "email": "lookup_email",
            "username": "lookup_username"
        }
    )

    async def lookup_email(self, email: str) -> models.HttpResponse:
        """
        Look up an email on about.me to find the linked account.

        :param email:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="post",
            request_name="about_me_find_account",
            url="https://api.about.me/password/find_account",
            data={"email_address": email}
        )

    async def lookup_username(self, username: str) -> models.HttpResponse:
        """
        Look up a username on about.me to find the profile's information.

        :param username:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="about_me_username_lookup",
            url=f"https://about.me/{username}"
        )


class CompanyHouseScraper(Scraper):
    information = models.ScraperMetadata(
        name="Company House scraper",
        main_url="https://find-and-update.company-information.service.gov.uk/",
        functions={
            "fullname": "lookup_fullname"
        }
    )

    async def lookup_fullname(self, fullname: str) -> models.HttpResponse:
        """
        Look up a fullname on company house to find the person's information.

        :param fullname:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="company_house_fullname_lookup",
            url=f"https://find-and-update.company-information.service.gov.uk/search/officers?q={fullname}"
        )


class GravatarScraper(Scraper):
    information = models.ScraperMetadata(
        name="Gravatar scraper",
        main_url="https://gravatar.com/",
        functions={
            "email": "lookup_email"
        }
    )

    async def lookup_email(self, email: str) -> models.HttpResponse:
        """
        Look up an email on gravatar which is hashed then put into the path to get the person's profile.

        :param email:
        :return: models.HttpResponse
        """
        hashed_email = hashlib.md5(email.encode()).hexdigest()
        return await self.make_request(
            method="get",
            request_name="gravatar_email_lookup",
            url=f"https://en.gravatar.com/{hashed_email}.json"
        )


class DiscordScraper(Scraper):
    information = models.ScraperMetadata(
        name="Discord scraper",
        main_url="https://discord.com/",
        functions={
            "social_medias": "lookup_invite_code"
        }
    )

    async def lookup_invite_code(self, invite_url: str) -> models.HttpResponse | None:
        """
        Gets the inviter information from an invitation code to a discord server.

        :param invite_url:
        :return: models.HttpResponse
        """
        code = invite_url.split("discord.gg/")
        if len(code) != 2:
            return None

        return await self.make_request(
            method="get",
            request_name="discord_invite_code_lookup",
            url=f"https://discordapp.com/api/invite/{code[1]}"
        )


class PlanckeScraper(Scraper):
    information = models.ScraperMetadata(
        name="Plancke scraper",
        main_url="https://plancke.io/",
        functions={
            "minecraft_username": "lookup_minecraft_username"
        }
    )

    async def lookup_minecraft_username(
        self,
        minecraft_username: str
    ) -> models.HttpResponse:
        """
        Lookups information about a minecraft username on hypixel using Plancke.

        :param minecraft_username:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="plancke_minecraft_username_lookup",
            url=f"https://plancke.io/hypixel/player/stats/{minecraft_username}"
        )


SCRAPER_TUPLE = (
    AboutMeScraper,
    CompanyHouseScraper,
    GravatarScraper,
    DiscordScraper,
    PlanckeScraper
)
