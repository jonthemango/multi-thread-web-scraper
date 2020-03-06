from flask import Flask, Blueprint, request
import threading
from src.scraper.recursively_scrape import recursively_scrape
from src.models.Job import Job
from src.app import application, db

issue_job = Blueprint('issue_job', __name__)


@issue_job.route('/', defaults={'number_of_threads': 1})
@issue_job.route('/<int:number_of_threads>', methods=["GET", "POST"])
def main(number_of_threads):
    if request.method == "POST":

        urls = request.json["urls"]
        print(urls)

        threads = []
        for i in range(number_of_threads):
            t = threading.Thread(target=recursively_scrape, args=(urls))
            threads.append(t)
            t.start()
        print(threads)

        # Add job
        job = Job(number_of_threads=number_of_threads)
        db.session.add(job)
        db.session.commit()

        return {
            "job_id": job.get_id(),
            "threads": number_of_threads,
            "urls": urls
        }
    else:
        return {"status": "OK"}




    