from flask import Blueprint, request, current_app
from application.core.ServiceResponse import ServiceResponse
from application.cache.BaseCache import BaseCache
from application.cache.CacheType import CacheType

test_controller = Blueprint('test_controller', __name__, url_prefix='/api/test')


@test_controller.route('/cache', methods=['GET'])
def test():
    cache_param = {
        "user_id": "test"
    }
    value = BaseCache.instance().get(CacheType.UserInfo, cache_param)
    if not value:
        BaseCache.instance().set(CacheType.UserInfo, cache_param, "test")
    else:
        BaseCache.instance().delete(CacheType.UserInfo, cache_param)
    return 'ok'
