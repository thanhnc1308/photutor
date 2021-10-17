from flask import Blueprint

user_controller = Blueprint("user_controller", __name__, url_prefix='/api/users')


@user_controller.route('/')
def get_all():
    pass


@user_controller.route('/')
def get_by_id():
    pass


@user_controller.route('/')
def get_paging():
    pass


@user_controller.route('/')
def add():
    pass


@user_controller.route('/')
def update():
    pass
