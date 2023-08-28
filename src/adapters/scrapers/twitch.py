from src.adapters.scrapers import base_scraper
from src.domain import models


class TwitchScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Twitch scraoer",
        main_url="https://twitch.tv",
        functions={
            "social_medias": "lookup_twitch_profile"
        }
    )

    async def lookup_twitch_profile(self, link: str) -> models.HttpResponse | None:
        """
        Fetches the twitch profiles about me and returns the html

        :param link:
        :return: models.HttpResponse | None
        """
        split_link = link.split("twitch.tv/")
        if len(split_link) != 2:
            return None

        return await self.make_request(
            method="get",
            request_name="twitch_about_me_lookup",
            url=f"https://m.twitch.tv/{split_link[1]}/about"
        )
