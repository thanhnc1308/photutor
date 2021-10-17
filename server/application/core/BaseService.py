from flask import request, url_for
from sqlalchemy import desc
from http import HTTPStatus
from application.core.helpers import verify_token
from application.core.ServiceResponse import ServiceResponse


class BaseService:
    model = None
    schema = None
    list_schema = None
    paging_schema = None

    @verify_token
    def get_by_id(current_user, self, id=None):
        res = ServiceResponse()
        try:
            data = self.model.get_by_id(id)
            if not data:
                res.on_error(code=HTTPStatus.NOT_FOUND, user_message="Not found")
            res.on_success(data=self.schema.dump(data))
        except Exception as e:
            res.on_exception(e)
        return res.build()

    @verify_token
    def put(current_user, self, id):
        res = ServiceResponse()
        try:
            data = self.model.query.filter_by(id=id).first()
            if not data:
                res.on_error(code=HTTPStatus.NOT_FOUND, user_message="Not found")
            parameters = request.json
            errors = self.schema.validate(parameters)
            if errors:
                res.on_error(user_message=str(errors))
            data.update(**parameters)
            res.on_success(data=self.schema.dump(data))
        except Exception as e:
            res.on_exception(e)
        return res.build()

    @verify_token
    def delete(current_user, self, id):
        res = ServiceResponse()
        try:
            data = self.model.query.filter_by(id=id).first()
            if not data:
                res.on_error(code=HTTPStatus.NOT_FOUND, user_message="Not found")
            data.delete()
            res.on_success(data=self.schema.dump(data))
        except Exception as e:
            res.on_exception(e)
        return res.build()

    @verify_token
    def get_all(current_user, self):
        res = ServiceResponse()
        try:
            order_by = request.args.get('order_by', 'updated_at', type=str)
            data = self.model.get_all(order_by=order_by, user_id=current_user.get('id'))
            res.on_success(data=self.list_schema.dump(data))
        except Exception as e:
            res.on_exception(e)
        return res.build()

    @verify_token
    def get_paging(current_user, self):
        res = ServiceResponse()
        try:
            order_by = request.args.get('order_by', 'updated_at', type=str)
            max_per_page = 100
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)
            p = self.model.query.order_by(desc(order_by))\
                .filter_by(user_id=current_user.get('id'))\
                .paginate(page, per_page)

            meta = {
                'page': page,
                'per_page': per_page,
                'total': p.total,
                'pages': p.pages,
            }

            links = {}
            if p.has_next:
                links['next'] = url_for(request.endpoint, page=p.next_num,
                                        per_page=per_page)
            if p.has_prev:
                links['prev'] = url_for(request.endpoint, page=p.prev_num,
                                        per_page=per_page)
            links['first'] = url_for(request.endpoint, page=1,
                                     per_page=per_page)
            links['last'] = url_for(request.endpoint, page=p.pages,
                                    per_page=per_page)

            meta['links'] = links
            result = {
                'items': p.items,
                'meta': meta
            }
            res.on_success(data=self.paging_schema.dump(result))
        except Exception as e:
            res.on_exception(e)
        return res.build()

    @verify_token
    def post(current_user, self):
        res = ServiceResponse()
        try:
            parameters = request.json
            errors = self.schema.validate(parameters)
            if errors:
                res.on_error(user_message=str(errors))
            if 'user_id' not in parameters:
                parameters['user_id'] = current_user['id']
            new_item = self.model.create(**parameters)
            res.on_success(data=self.schema.dump(new_item))
        except Exception as e:
            res.on_exception(e)
        return res.build()
