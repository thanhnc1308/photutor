from flask import Blueprint, request, current_app
from application.core.extensions import mem_cache, redis_cache
from application.core.ServiceResponse import ServiceResponse

test_controller = Blueprint('test_controller', __name__, url_prefix='/api/test')


@test_controller.route('/test/<string:id>', methods=['GET'])
def test(id):
    print('id:', id)
    mem = mem_cache.get(id)
    if mem:
        return 'get from mem'
    r = redis_cache.get(id)
    if r:
        return 'get from redis'
    mem_cache.set(id, 'test')
    redis_cache.set(id, 'test')
    return 'new'
