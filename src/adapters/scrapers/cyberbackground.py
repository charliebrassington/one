from src.adapters.scrapers import base_scraper
from src.domain import models


class CyberScraper(base_scraper.CloudflareScraper):
    information = models.ScraperMetadata(
        name="Cyber Background Check scraper",
        main_url="https://www.cyberbackgroundchecks.com/",
        functions={
            "email": "lookup_email",
            "cyber_person_id": "lookup_person"
        }
    )

    async def lookup_email(self, email: str) -> models.HttpResponse:
        """
        Lookups an email on cyberbackgroundchecks.com to find the person the email is registered to.

        :param email:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="cyberbackgroundcheck_email_lookup",
            url=f"https://www.cyberbackgroundchecks.com/email/{email}"
        )

    async def lookup_person(self, cyber_person_id: str) -> models.HttpResponse:
        """
        Lookups the person id which is scraped from a search

        :param cyber_person_id:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="cyberbackgroundcheck_person_id_lookup",
            url=f"https://www.cyberbackgroundchecks.com/detail/{cyber_person_id}"
        )
