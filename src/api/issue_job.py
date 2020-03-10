from flask import Flask, Blueprint, request
import threading
from multiprocessing.dummy import Pool
from src.scraper.recursively_scrape import recursively_scrape
from src.models.Job import Job, UrlTask, UrlImageMapping
from src.app import application, db
from src.utils.threading_utils import ThreadPool
issue_job = Blueprint('issue_job', __name__)


def handle_url(url_job_tuple):
    # get id
    url_task_id, job_id = url_job_tuple

    # get the task and job
    url_task = UrlTask.query.filter_by(id=url_task_id).first()
    job = Job.query.filter_by(id=job_id).first()

    application.logger.info("Handling URL Task: " + url_task.site_url)

    # scrape the url
    image_urls = recursively_scrape(url_task.site_url)
    application.logger.info("Got Image Urls: " + url_task.site_url)

    # for each image in list, add associated mapping to db
    for image_url in image_urls:
        mapping = UrlImageMapping(job_id=job.id, task_id=url_task.id, site_url=url_task.site_url, image_url=image_url)
        db.session.add(mapping)
    
    # set task as done
    url_task.set_done()

    # commit changes to db
    db.session.commit()
    application.logger.info("Task is completed: " + url_task.site_url)

    



@issue_job.route('/<int:number_of_threads>', methods=["GET", "POST"])
@issue_job.route('/', defaults={'number_of_threads': 1}, methods=["GET", "POST"])
def main(number_of_threads):
    if request.method == "POST":
        urls = request.json["urls"]
        
        # Add a job
        job = Job(number_of_threads=number_of_threads,urls=urls)
        application.logger.info("Incoming request. Starting job: " + job.id)


        db.session.add(job)
        db.session.commit()

        url_job_tuples = list(map(lambda url: (url, job.id), urls))

        url_job_tasks = list(map(lambda task: (task.id, job.id), job.get_tasks()))

        

        threads = []

        tp = ThreadPool(number_of_threads = number_of_threads)

        for url_job_tuple in url_job_tasks:
            tp.add_task(handle_url, url_job_tuple)

        return {
            "job_id": job.get_id(),
            "threads": number_of_threads,
            "urls": urls
        }
    else:
        return {"status": "OK"}




    