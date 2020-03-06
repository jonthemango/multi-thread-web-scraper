from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)


# Import API blue prints and register them to the application
from src.api.issue_job import issue_job
application.register_blueprint(issue_job)