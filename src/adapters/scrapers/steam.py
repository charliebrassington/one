from src.adapters.scrapers import base_scraper
from src.domain import models


class SteamScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Steam scraper",
        main_url="https://steamcommunity.com/",
        functions={
            "steam_id": "lookup_steam_id",
            "social_medias": "lookup_steam_link"
        }
    )

    async def lookup_steam_id(self, steam_id: str) -> models.HttpResponse:
        """
        Lookups a steam ID and returns the http response collected.

        :param steam_id:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="steam_id_lookup",
            url=f"https://steamcommunity.com/id/{steam_id}"
        )

    async def lookup_steam_link(self, link: str) -> models.HttpResponse | None:
        """
        Wrapper for lookup_steam_id if a steam profile is found.

        :param link:
        :return: models.HttpResponse
        """
        if "steamcommunity" not in link:
            return None

        return await self.lookup_steam_id(steam_id=link.split("id/")[1].split("/")[0])
