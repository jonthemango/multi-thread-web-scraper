from flask import Flask, Blueprint, request
import threading
from multiprocessing.dummy import Pool
from src.scraper.recursively_scrape import recursively_scrape
from src.models.Job import Job, UrlTask, UrlImageMapping
from src.app import application, db
from src.utils.threading_utils import ThreadPool
issue_job = Blueprint('issue_job', __name__)


def handle_url(url_job):
    url, job_id = url_job
    print("Handling URL")
    job = Job.query.filter_by(id=job_id).first()
    image_urls = recursively_scrape(url)
    print("Get Image Urls")
    for image_url in image_urls:
        mapping = UrlImageMapping(job_id=job.id, site_url=url, image_url=image_url)
        db.session.add(mapping)
    task = job.get_task(url)
    task.set_done()
    print(task.completed)
    db.session.commit()
    



@issue_job.route('/', defaults={'number_of_threads': 1}, methods=["GET", "POST"])
@issue_job.route('/<int:number_of_threads>', methods=["GET", "POST"])
def main(number_of_threads):
    if request.method == "POST":

        urls = request.json["urls"]
        
        # Add a job
        job = Job(number_of_threads=number_of_threads,urls=urls)

        db.session.add(job)
        db.session.commit()
        url_job_tuples = list(map(lambda url: (url, job.id), urls))

        

        threads = []

        tp = ThreadPool(number_of_threads = number_of_threads)
        for url_job_tuple in url_job_tuples:
            tp.add_task(handle_url, url_job_tuple)

        return {
            "job_id": job.get_id(),
            "threads": number_of_threads,
            "urls": urls
        }
    else:
        return {"status": "OK"}




    