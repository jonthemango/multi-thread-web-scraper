from flask import Flask, Blueprint, request
import threading
from src.models.Job import Job
from src.app import application, db

get_job = Blueprint('get_job', __name__)


@get_job.route('/status/<string:job_id>', methods=["GET"])
def get_job_status(job_id):
    try:
        job = Job.query.filter_by(id=job_id).first()
        completed, in_progress = job.get_status()
        return {"completed": completed, "inProgress": in_progress}
    except:
        return {"error": "Job Id not found."}


@get_job.route('/result/<string:job_id>', methods=["GET"])
@get_job.route('/results/<string:job_id>', methods=["GET"])
def get_job_result(job_id):
    try:
        job = Job.query.filter_by(id=job_id).first()
        result = job.get_result()
        return result
    except:
        return {"error": "Job Id not found."}