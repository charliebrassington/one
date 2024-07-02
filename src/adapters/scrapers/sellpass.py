from src.adapters.scrapers import base_scraper
from src.domain import models


class SellpassScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Sellpass scraper",
        main_url="https://sellpass.io/",
        functions={
            "sellpass_username": "lookup_sellpass_store",
            "social_medias": "lookup_sellpass_link"
        }
    )

    async def lookup_sellpass_store(self, sellpass_username: str) -> models.HttpResponse:
        """
        Lookups and returns the sellpass store response for the given username.

        :param sellpass_username:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="sellpass_store_username_lookup",
            url=f"https://{sellpass_username}.sellpass.io/"
        )

    async def lookup_sellpass_link(self, link: str) -> models.HttpResponse | None:
        """
        Wrapper for lookup_sellpass_store inputting links instead of store names.

        :param link:
        :return: models.HttpResponse
        """
        link_split = link.split(".sellpass.")
        if len(link_split) != 2:
            return None

        return await self.lookup_sellpass_store(link_split[0].split("//")[1])
