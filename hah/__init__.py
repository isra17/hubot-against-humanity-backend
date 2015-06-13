from flask import Flask, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
from hah.plugins import rollbar, logging
import os

db = SQLAlchemy()

def create_app(config=None):
    global db

    app = Flask(__name__)
    app.config.from_object('config')
    if config:
        app.config.from_object(config)
    if 'ENV' in os.environ:
        app.config.from_object('config.{}'.format(os.environ['ENV']))

    logging.init_logging(app)

    db.init_app(app)

    rollbar.init_rollbar(app)

    from hah.api import Api
    Api(app)

    app.logger.info('[hah] App created')

    return app

