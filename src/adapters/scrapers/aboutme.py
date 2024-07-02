from src.adapters.scrapers import base_scraper
from src.domain import models


class AboutMeScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="About me scraper",
        main_url="https://about.me/",
        functions={
            "email": "lookup_email",
            "about_me_username": "lookup_username"
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
