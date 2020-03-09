from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
import logging 


application = Flask(__name__)
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)

gunicorn_logger = logging.getLogger("gunicorn.error")
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)

# Import API blue prints and register them to the application
from src.api.issue_job import issue_job
from src.api.get_job import get_job

application.register_blueprint(issue_job)
application.register_blueprint(get_job)