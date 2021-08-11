from app.models.candidate import Candidate
import json
import aiohttp
from urllib.error import HTTPError
from typing import TypeVar, Type, TypedDict
from graphql.error import GraphQLError

from app.models.fec_response import FecResponse
from app.utils.setup_logger import get_logger
from .secrets import BASE_URL, API_KEY

T = TypeVar('T', bound=TypedDict)


class FecApi():
    LOGGER = get_logger(__name__)

    @staticmethod
    def __parse_base_fec_response(data: json, dict_interface: Type[T]) -> FecResponse[T]:
        return FecResponse[dict_interface](data['results'], data['pagination'])

    @staticmethod
    async def get(url: str, dict_interface: Type[T]) -> FecResponse[T]:
        async with aiohttp.ClientSession() as session:
            url = f'{BASE_URL}{url}?api_key={API_KEY}'
            FecApi.LOGGER.info(f'Sending GET to {url}')

            async with session.get(url) as response:
                FecApi.LOGGER.info(f'Received {response.status} from {url}')

                ok = response.status < 399

                if not ok:
                    raise GraphQLError(
                        f'Received a {response.status} response from FEC server')

                data = await response.json()

                return FecApi.__parse_base_fec_response(data, dict_interface)
