from src.adapters.scrapers import base_scraper
from src.domain import models


class PlanckeScraper(base_scraper.Scraper):
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
