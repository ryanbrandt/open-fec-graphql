from graphene import ObjectType, String

from app.utils.setup_logger import get_logger
from app.utils.api import FecApi


class Query(ObjectType):
    LOGGER = get_logger(__name__)

    hello = String()

    async def resolve_hello(root, info):
        result = await FecApi.get('/candidate/P40006033')
        return result.results
