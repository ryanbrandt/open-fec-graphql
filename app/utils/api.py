import aiohttp
import os
from typing import TypeVar, Type, TypedDict
from graphql.error import GraphQLError
from flask import request

from app.models.fec_response import FecResponse
from .setup_logger import get_logger

T = TypeVar('T', bound=TypedDict)

API_KEY_PARAM = 'api_key'

API_TIMEOUT = 2000


class FecApi():
    LOGGER = get_logger(__name__)

    @staticmethod
    async def get(url: str, dict_interface: Type[T], params: dict = {}) -> FecResponse[T]:
        if API_KEY_PARAM not in request.args:
            raise GraphQLError('API key is required')

        auth_params = {
            API_KEY_PARAM: request.args[API_KEY_PARAM]
        }
        merged_params = params | auth_params

        session_timeout = aiohttp.ClientTimeout(
            total=None, sock_connect=API_TIMEOUT / 2, sock_read=API_TIMEOUT)

        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            BASE_URL = os.environ['FEC_BASE_URL']
            full_url = f'{BASE_URL}{url}'

            FecApi.LOGGER.info(
                f'Sending GET to {full_url} with params {merged_params}')

            async with session.get(full_url, params=merged_params) as response:
                FecApi.LOGGER.info(
                    f'Received {response.status} from {full_url}')

                ok = response.status < 399

                if not ok:
                    raise GraphQLError(
                        f'Received a {response.status} response from FEC server')

                data = await response.json()

                return FecResponse[dict_interface](data['results'], data['pagination'])
