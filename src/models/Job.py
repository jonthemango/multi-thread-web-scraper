from src.app import application, db
import uuid

class Job (db.Model):
    id = db.Column(db.String(100), primary_key=True)
    number_of_threads = db.Column(db.Integer)

    def __init__(self, number_of_threads):
        self.id = str(uuid.uuid1())
        self.number_of_threads = number_of_threads

    def get_id(self):
        return self.id


class JobImageMapping (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(100))
    site_url = db.Column(db.String(2000))
    image_url = db.Column(db.String(2000))

db.create_all()