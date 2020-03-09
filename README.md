# multi-thread-web-scraper
Multi-threading Web Scraper

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

## Contracts

```
curl --location --request GET 'http://192.168.99.100:5000/'
{"status":"OK"}
```

```
curl --location --request POST 'http://192.168.99.100:5000/4' --header 'Content-Type: application/json' --data-raw '{
"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}' 

{"job_id":"59035db6-61ce-11ea-9dbf-0242ac110002","threads":4,"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}
```

```
curl --location --request POST 'http://192.168.99.100:5000/' --header 'Content-Type: application/json' --data-raw '{
"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}' 

{"job_id":"585c5656-6237-11ea-8a0a-0242ac110002","threads":1,"urls":["https://docs.python.org/3/library/threading.html", "https://stackoverflow.com/"]}
```

```
curl --location --request GET 'http://192.168.99.100:5000/status/585c5656-6237-11ea-8a0a-0242ac110002'

{"completed": <int>,"inProgress": <int>}
```

```
curl --location --request GET 'http://192.168.99.100:5000/result/585c5656-6237-11ea-8a0a-0242ac110002'

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

## Arch and Design


