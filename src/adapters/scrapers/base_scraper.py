import aiohttp
import tls_client

from abc import ABC, abstractmethod
from src.domain import models


class AbstractScraper(ABC):

    @abstractmethod
    async def make_request(
        self,
        method: str,
        request_name: str,
        **kwargs
    ) -> models.HttpResponse:
        raise NotImplementedError


class Scraper(AbstractScraper):
    information: models.ScraperMetadata

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def make_request(
        self,
        method: str,
        request_name: str,
        **kwargs
    ) -> models.HttpResponse:
        """
        Making requests with the session.

        :param method:
        :param request_name:
        :param kwargs:
        :return: models.HttpResponse
        """
        async with getattr(self.session, method)(**kwargs, timeout=5) as response:
            content = await response.text()
            return models.HttpResponse(
                name=request_name,
                content=content,
                status_code=response.status
            )


class CloudflareScraper(AbstractScraper):
    information: models.ScraperMetadata

    def __init__(self, **kwargs):
        """
        Allowing arguments to make sure it doesn't error when the service passes an aiohttp client into the constructor.

        :param kwargs:
        """
        self.session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )

    async def make_request(
        self,
        method: str,
        request_name: str,
        **kwargs
    ) -> models.HttpResponse:
        """
        Making a request using the tls_client module to bypass cloudflare

        :param method:
        :param request_name:
        :param kwargs:
        :return: models.HttpResponse
        """
        response = getattr(self.session, method)(**kwargs)
        return models.HttpResponse(
            name=request_name,
            content=response.text,
            status_code=response.status_code
        )
