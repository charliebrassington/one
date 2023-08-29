from src.adapters.scrapers import base_scraper
from src.domain import models

from aiohttp import ClientSession


class YoutubeScraper(base_scraper.Scraper):
    _completed_consent_form = False
    information = models.ScraperMetadata(
        name="Youtube scraper",
        main_url="https://youtube.com",
        functions={
            "social_medias": "lookup_youtube_channel",
            "consent_form_url": "complete_consent_form"
        }
    )

    async def lookup_youtube_channel(self, link: str) -> models.HttpResponse | None:
        """
        Checks to see if the link passed is a YouTube channel and fetches the HTML.

        :param link:
        :return: models.HttpResponse | None
        """
        if "youtube.com/channel" not in link:
            return None

        if not link.endswith("/about"):
            link = f"{link}/about"

        return await self.make_request(
            method="get",
            request_name="youtube_channel_lookup" if YoutubeScraper._completed_consent_form else "consent_form_lookup",
            url=link
        )

    async def complete_consent_form(self, link: str) -> models.HttpResponse:
        """
        Takes a consent form URL gets the channel then submits the form then fetches channel response.

        :param link:
        :return: models.HttpResponse
        """
        consent_url, channel = link.split("split-point")
        await self.make_request(
            method="post",
            request_name="null",
            url=consent_url,
            data={}
        )

        YoutubeScraper._completed_consent_form = True
        return await self.lookup_youtube_channel(link=channel.replace("?cbrd=1", "/about"))
