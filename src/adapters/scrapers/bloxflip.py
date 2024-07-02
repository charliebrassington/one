from src.adapters.scrapers import base_scraper
from src.domain import models


class BloxflipScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Bloxflip scraper",
        main_url="https://bloxflip.com/",
        functions={
            "roblox_id": "lookup_roblox_id"
        }
    )

    async def lookup_roblox_id(self, roblox_id: str) -> models.HttpResponse:
        return await self.make_request(
            method="get",
            request_name="bloxflip_roblox_id_lookup",
            url=f"https://api.bloxflip.com/user/lookup/{roblox_id}",
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S906E) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"
            }
        )
