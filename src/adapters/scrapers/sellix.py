from src.adapters.scrapers import base_scraper
from src.domain import models


class SellixScraper(base_scraper.CloudflareScraper):
    information = models.ScraperMetadata(
        name="Sellix scraper",
        main_url="https://mysellix.io/",
        functions={
            "sellix_username": "lookup_sellix_store",
            "social_medias": "lookup_sellix_link"
        }
    )

    async def lookup_sellix_store(self, sellix_username: str) -> models.HttpResponse:
        """
        Lookups and returns the sellix store response for the given username.

        :param sellix_username:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="sellix_store_username_lookup",
            url=f"https://{sellix_username}.mysellix.io"
        )

    async def lookup_sellix_link(self, link: str) -> models.HttpResponse | None:
        """
        Wrapper for lookup_sellpass_store inputting links instead of store names.

        :param link:
        :return: models.HttpResponse
        """
        if "sellix" not in link:
            return None

        url_split = link.split(".")
        return await self.lookup_sellix_store(url_split[0].split("://")[1])
