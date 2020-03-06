import requests


def recursively_scrape(url, max_depth=2):
    x = len(requests.get(url).content) # basic "scraper" right now
    print(x)
    return x