from src.adapters.scrapers import base_scraper
from src.domain import models


class MailruScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="About me scraper",
        main_url="https://about.me/",
        functions={
            "email": "recover_email",
        }
    )

    async def recover_email(self, email: str) -> models.HttpResponse | None:
        """
        Finds email and phone number hints for the recovery account from a mail.ru account.

        :param email:
        :return: models.HttpResponse
        """
        if not email.endswith("mail.ru"):
            return None

        return await self.make_request(
            method="post",
            request_name="mail_ru_recovery_result",
            url="https://account.mail.ru/api/v1/user/password/restore",
            data={"email": email, "htmlencoded": "false"}
        )
