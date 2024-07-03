from src.adapters.scrapers.base_scraper import CloudflareScraper
from src.domain import models


class VirginMediaScraper(CloudflareScraper):
    postcode = None
    information = models.ScraperMetadata(
        name="Virgin Media scraper",
        main_url="https://www.virginmedia.com/",
        functions={
            "postcode": "cache_postcode",
            "last_name": "check_if_household_exists",
            "services_conversation_id": "get_services",
            "faults_conversation_id": "get_broadband_info"
        }
    )

    def __init__(self, **kwargs):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en;q=0.5',
            'DAPI-CorrelationID': '2bca2910-c022-40f0-9e97-d978e06c4e68',
            'DAPI-RequestID': '2bca2910-c022-40f0-9e97-d978e06c4e68',
            'DAPI-RequestTimestamp': '2024-06-24T13:58:34.801Z',
            'DAPI-ChannelID': 'Care-SelfCare-WEB',
            'DAPI-OriginatorID': '2bca2910-c022-40f0-9e97-d978e06c4e68',
            'Content-Type': 'application/json; charset=utf-8',
            'DAPI-ClientSecret': 'lnlzYDi9zqxr7NiLS1N7YZPZ1tNN27uK1yY7ktRveZZGAMhaRGmkNd3o3iQRQHI8',
            'DAPI-AppID': 'PR2HJ4yVbIK6vg0uQLXvqR1GjNX40gLOxkFoKMYeGGlGBrZC',
            'x-dtc': 'sn=v_4_srv_5_sn_R497QRIU1JDUU8IBD3Q5P1EGSFA7O23Q, pc=5$237508251_327h13vDLDQLMDHPNBQVCTFBSLVKTMKUVNSASFP-0e0, v=1718823822690P80VJ3H9NHEK06KG5HB25SD7LBTBUJ66, app=2d0383d7e551004e, r=https://www.virginmedia.com/help/check/status/identification/identify, sn=v_4_srv_5_sn_R497QRIU1JDUU8IBD3Q5P1EGSFA7O23Q, pc=5$237508251_327h13vDLDQLMDHPNBQVCTFBSLVKTMKUVNSASFP-0e0, v=1718823822690P80VJ3H9NHEK06KG5HB25SD7LBTBUJ66, app=2d0383d7e551004e, r=https://www.virginmedia.com/help/check/status/identification/identify',
            'Origin': 'https://www.virginmedia.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.virginmedia.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

    async def cache_postcode(self, postcode: str) -> None:
        VirginMediaScraper.postcode = postcode
        return None

    async def check_if_household_exists(self, last_name: str) -> models.HttpResponse | None:
        if VirginMediaScraper.postcode is None:
            return None

        return await self.make_request(
            method="post",
            request_name="virgin_media_check_household",
            url="https://api.vmo2digital.co.uk/faults/workflow/v1/identify",
            json={"postCode": VirginMediaScraper.postcode, "lastName": last_name},
            headers=self.headers
        )

    def _new_headers(self, convo_id: str) -> dict:
        headers = self.headers.copy()
        headers["DAPI-ConversationId"] = convo_id
        return headers

    async def get_services(self, service_convo_id: str) -> models.HttpResponse:
        return await self.make_request(
            method="get",
            request_name="virgin_media_get_services",
            url="https://api.vmo2digital.co.uk/faults/workflow-service-status/v1",
            headers=self._new_headers(service_convo_id)
        )

    async def get_broadband_info(self, faults_convo_id: str) -> models.HttpResponse:
        return await self.make_request(
            method="post",
            request_name="virgin_media_get_broadband_info",
            url="https://api.vmo2digital.co.uk/faults/workflow/v1",
            json={"productTypes": ["BB"]},
            headers=self._new_headers(faults_convo_id)
        )
