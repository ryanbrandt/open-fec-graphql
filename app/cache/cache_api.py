from flask import Blueprint
from flask_cors import cross_origin

from app.utils.setup_logger import get_logger
from .cache import cache

cache_api = Blueprint('cache_api', __name__)

LOGGER = get_logger(__name__)


@cache_api.route('/cache', methods=['DELETE'])
@cross_origin()
def clear_cache():
    try:
        cache.flushall()
    except Exception as e:
        LOGGER.error(e)
        return 'Failed to clear cache', 500

    return 'Successfully cleared cache', 204
