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
