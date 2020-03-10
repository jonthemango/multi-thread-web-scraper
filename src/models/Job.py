from src.app import application, db
import uuid

class Job (db.Model):
    id = db.Column(db.String(100), primary_key=True)
    number_of_threads = db.Column(db.Integer)

    def __init__(self, number_of_threads, urls):
        self.id = str(uuid.uuid1())
        self.number_of_threads = number_of_threads
        for url in urls:
            db.session.add(UrlTask(job_id=self.id, site_url=url))

    def get_id(self):
        return self.id

    def get_status(self):
        url_tasks = UrlTask.query.filter_by(job_id=self.id).all()
        completed = 0
        in_progress = 0
        for task in url_tasks:
            if task.completed == 1:
                completed = completed + 1
            else:
                in_progress = in_progress + 1
        return completed, in_progress
    
    def get_result(self):
        # get all site urls (UrlTask) associated with the job_id
        url_tasks = UrlTask.query.filter_by(job_id=self.id).all()

        result = {}
        # for each url task, if completed then get list of urls and assign to the site url
        for task in url_tasks:
            if task.completed == 1:
                url_result = task.get_result()
                result[task.site_url] = url_result
            else:
                result[task.site_url] = []
        return result
    
    def get_task(self, site_url):
        return UrlTask.query.filter_by(job_id=self.id, site_url=site_url).first()      
    
    def get_tasks(self):
        return UrlTask.query.filter_by(job_id=self.id).all()





class UrlTask (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(100))
    site_url = db.Column(db.String(2000))
    completed = db.Column(db.Integer, default=0)

    def get_result(self):
        # get all UrlImageMappings where job_id and site_url match
        image_mappings = UrlImageMapping.query.filter_by(job_id=self.job_id, task_id=self.id).all()

        # map that object to a list of urls
        list_of_image_urls = list(map(lambda imageMapping: imageMapping.image_url, image_mappings))

        return list_of_image_urls
    
    def set_done(self):
        self.completed = 1


class UrlImageMapping (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(100))
    task_id = db.Column(db.Integer)
    site_url = db.Column(db.String(2000))
    image_url = db.Column(db.String(2000))

db.create_all()