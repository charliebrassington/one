from src.adapters.scrapers import base_scraper
from src.domain import models

import asyncio


class NitterScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Nitter scraper",
        main_url="https://nitter.net/",
        functions={
            "social_medias": "lookup_nitter_profile"
        }
    )

    async def lookup_nitter_profile(self, link: str) -> models.HttpResponse | None:
        """
        Gets the response from nitter when fetching the users profile.

        :param link:
        :return: models.HttpResponse
        """
        link_split = link.split("twitter.com/")
        if len(link_split) != 2:
            return None

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S906E) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

        try:
            return await self.make_request(
                method="get",
                request_name="nitter_profile_lookup",
                url=f"https://nitter.net/{link_split[1]}",
                headers=headers
            )

        except asyncio.TimeoutError:
            return None
