import hashlib

from src.adapters.scrapers import base_scraper
from src.domain import models


class GravatarScraper(base_scraper.Scraper):
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
