from queue import Queue
from threading import Thread


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            func(*args, **kargs)
            self.tasks.task_done()





class ThreadPool:
    def __init__(self, number_of_threads):
        self.tasks = Queue(number_of_threads)
        
        for i in range(number_of_threads):
            worker = Worker(self.tasks)
            worker.start()

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()