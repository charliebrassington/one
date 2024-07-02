from src.adapters.scrapers import base_scraper
from src.domain import models


class TelegramScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Telegram scraper",
        main_url="https://t.me",
        functions={
            "social_medias": "lookup_telegram_channel"
        }
    )

    async def lookup_telegram_channel(self, link: str) -> models.HttpResponse | None:
        link_split = link.split("t.me/")
        if len(link_split) != 2:
            return None

        return await self.make_request(
            method="get",
            request_name="telegram_channel_lookup",
            url=f"https://t.me/s/{link_split[1]}"
        )

