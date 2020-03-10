# Multi-threading Web Scraper
This application starts a web server at port 5000 which accepts requests containing a list of urls and a number of threads (N). It responds with a job id that users can use to query the status/result of the job. Each url is treated as a task and is add to a thread pool containing N available workers. The ThreadPool uses non-blocking threading which allows a quick response for API requests. The workers process each url by visiting the web page associated with it, collecting the src of all `<img>` tags on the page as well as the src of all `<img>` tags on every page referenced by an `<a>` tag. It does this recursively (currently set to max depth of 2). Users can then use the job id to query the status and results of the job.

The application is built using Python 3.7, Python flask framework, gunicorn for launching the web server, the Python threading module, Beautiful Soup for parsing HTML responses, flask-SQLalchemy as an ORM for a basic SQLite database and Docker.

There are several design improvements that could be made. For one, currently the database is SQLite which resides as a file on disk inside of the docker image. This could be improved by allowing connections to an outside database connection, allowing this docker image to scale to multiple instances. Another possible improvement would be to restart URL tasks if threads/gunicorn workers die. Currently, if processing of the tasks are dropped, they are not re-issued to completion.

# Docker

## Build
```
docker build -t crawler_test -f Dockerfile ./
```

## Run
```
docker run --name ct -p 5000:5000 crawler_test
```

## Kill and Remove 
```
docker kill ct
docker rm ct    
```

# Contracts

## GET /
```
curl --location --request GET 'http://localhost:5000/'
{"status":"OK"}
```

## POST /N {urls}
```
curl --location --request POST 'http://localhost:5000/4' --header 'Content-Type: application/json' --data-raw '{
"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}' 

{"job_id":"59035db6-61ce-11ea-9dbf-0242ac110002","threads":4,"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}
```

## POST / {urls}
```
curl --location --request POST 'http://localhost:5000/' --header 'Content-Type: application/json' --data-raw '{
"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}' 

{"job_id":"585c5656-6237-11ea-8a0a-0242ac110002","threads":1,"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}
```

## GET /status/id
```
curl --location --request GET 'http://localhost:5000/status/585c5656-6237-11ea-8a0a-0242ac110002'

{"completed": <int>,"inProgress": <int>}
```

## GET /result/id
```
curl --location --request GET 'http://localhost:5000/result/585c5656-6237-11ea-8a0a-0242ac110002'

{
    "https://stackoverflow.com/questions/7983820/get-the-last-4-characters-of-a-string": [
        "https://i.stack.imgur.com/ImYIK.jpg?s=32&g=1",
        "https://www.gravatar.com/avatar/e27e02f7a1eb398582994b9bd2d1a696?s=32&d=identicon&r=PG",
        "https://i.stack.imgur.com/FDsmS.png?s=32&g=1",
        "https://www.gravatar.com/avatar/4ac67b333bfad69fec3396dfc40c66c0?s=32&d=identicon&r=PG",
        "https://i.stack.imgur.com/Pem8D.jpg?s=32&g=1",
    ],
    ...
```

# Arch and Design
The container launches 4 gunicorn workers for handling incoming requests. When a POST request is issued to the docker container at port 5000, the container forwards the request to its localhost:5000 where one of the gunicorn workers process the request.

Gunicorn processes the request using flask. The route POST /N creates a thread pool of size N and for each url in its body, it adds a task to the thread pool. The API immediately responds with the job id.
![image](https://user-images.githubusercontent.com/10063663/76257610-64f1bf00-6228-11ea-81f6-af2c1bfa0d2d.png)


# Python Installation

## Install
```
git clone https://github.com/jonthemango/multi-thread-web-scraper.git
cd multi-thread-web-scraper
pip install -r requirements.txt
python main.py
```



