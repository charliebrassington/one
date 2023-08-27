import aiohttp
import json

from typing import Type
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
        print(f"Sent request {request_name}")
        """
        Making requests with the session.

        :param method:
        :param request_name:
        :param kwargs:
        :return: models.HttpResponse
        """
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


SCRAPER_TUPLE = (
    AboutMeScraper,
    CompanyHouseScraper
)
