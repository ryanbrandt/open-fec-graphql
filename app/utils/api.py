import aiohttp
from typing import Dict, TypeVar, Type, TypedDict
from graphql.error import GraphQLError
from flask import request

from app.models.fec_response import FecResponse
from .setup_logger import get_logger
from .secrets import BASE_URL

T = TypeVar('T', bound=TypedDict)

API_KEY_PARAM = 'api_key'


class FecApi():
    LOGGER = get_logger(__name__)

    @staticmethod
    async def get(url: str, dict_interface: Type[T], params: Dict = {}) -> FecResponse[T]:
        if API_KEY_PARAM not in request.args:
            raise GraphQLError('API key is required')

        auth_params = {
            API_KEY_PARAM: request.args[API_KEY_PARAM]
        }
        merged_params = params | auth_params

        async with aiohttp.ClientSession() as session:
            url = f'{BASE_URL}{url}'
            FecApi.LOGGER.info(
                f'Sending GET to {url} with params {merged_params}')

            async with session.get(url, params=merged_params) as response:
                FecApi.LOGGER.info(f'Received {response.status} from {url}')

                ok = response.status < 399

                if not ok:
                    raise GraphQLError(
                        f'Received a {response.status} response from FEC server')

                data = await response.json()

                return FecResponse[dict_interface](data['results'], data['pagination'])
