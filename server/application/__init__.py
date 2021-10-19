from flask import Flask
from flask_sqlalchemy import get_debug_queries
from werkzeug.exceptions import default_exceptions
from application.core.extensions import db, cors, jwt, migrate
from application.controllers.UserController import user_controller
from application.controllers.AuthController import auth_controller


def create_app(config_name):
    app = Flask(__name__)
    configure_app(app, config_name)
    configure_hook(app)
    configure_blueprint(app)
    configure_extensions(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        return {
            "message": str(e)
        }

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    @app.route("/")
    def hello_world():
        return 'Hello'

    return app


def configure_app(app, config_name=None):
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)


def configure_hook(app):
    # app.after_request(sql_debug)
    pass


def configure_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)


def configure_blueprint(app):
    app.register_blueprint(user_controller)
    app.register_blueprint(auth_controller)


def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n    ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(total_duration * 1000, 2))

    print('=' * 80)
    print('SQL Queries: - {0}\nQueries executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')
    return response
