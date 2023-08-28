from src.adapters.scrapers import base_scraper
from src.domain import models


class CompanyHouseScraper(base_scraper.Scraper):
    information = models.ScraperMetadata(
        name="Company House scraper",
        main_url="https://find-and-update.company-information.service.gov.uk/",
        functions={
            "fullname": "lookup_fullname"
        }
    )

    async def lookup_fullname(self, fullname: str) -> models.HttpResponse:
        """
        Look up a fullname on company house to find the person's information.

        :param fullname:
        :return: models.HttpResponse
        """
        return await self.make_request(
            method="get",
            request_name="company_house_fullname_lookup",
            url=f"https://find-and-update.company-information.service.gov.uk/search/officers?q={fullname}"
        )
