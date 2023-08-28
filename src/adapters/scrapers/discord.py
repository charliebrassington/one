from src.adapters.scrapers import base_scraper
from src.domain import models


class DiscordScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Discord scraper",
        main_url="https://discord.com/",
        functions={
            "social_medias": "lookup_invite_code"
        }
    )

    async def lookup_invite_code(self, invite_url: str) -> models.HttpResponse | None:
        """
        Gets the inviter information from an invitation code to a discord server.

        :param invite_url:
        :return: models.HttpResponse | None
        """
        code = invite_url.split("discord.gg/")
        if len(code) != 2:
            return None

        return await self.make_request(
            method="get",
            request_name="discord_invite_code_lookup",
            url=f"https://discordapp.com/api/invite/{code[1]}"
        )
