from src.domain import models
from src.adapters.scrapers import base_scraper


class DuolingoScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Duolingo scraper",
        main_url="https://www.duolingo.com/",
        functions={
            "email": "lookup_email"
        }
    )

    async def lookup_email(self, email: str) -> models.HttpResponse:
        """
        Lookup an email on duolingo.com to find the profile matching the email if signed up.

        :param email:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="duolingo_email_lookup",
            url=f"https://duolingo.com/2017-06-30/users?email={email}",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"}
        )
