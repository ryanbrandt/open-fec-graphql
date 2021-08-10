import json
import aiohttp
from urllib.error import HTTPError

from app.models.fec_response import FecResponse
from app.utils.setup_logger import get_logger
from .secrets import BASE_URL, API_KEY


class FecApi():
    LOGGER = get_logger(__name__)

    @staticmethod
    def __parse_base_fec_response(data: json):
        return FecResponse(data['results'], data['pagination'])

    @staticmethod
    async def get(url: str) -> FecResponse:
        async with aiohttp.ClientSession() as session:
            url = f'{BASE_URL}{url}?api_key={API_KEY}'
            FecApi.LOGGER.info(f'Sending GET to {url}')

            async with session.get(url) as response:
                FecApi.LOGGER.info(f'Received {response.status} from {url}')

                ok = response.status < 399
                data = await response.json()

                if not ok:
                    raise HTTPError('Received a non-OK response')

                return FecApi.__parse_base_fec_response(data)
