import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.app import application, db


image_extensions = ['.png', '.gif', '.jpg', '.svg']
def recursively_scrape(url, current_depth=1, max_depth=2):

    if current_depth == 1:
        application.logger.info("Querying: " + url)



    try:
        # query the url, if theres an error then return empty list
        html = requests.get(url).text # basic "scraper" right now
    except:
        return []
    
    
    # make an html parser and setup an empty list
    soup = BeautifulSoup(html, 'html.parser')
    url_list = []

    # get all image tags, get their absolute source and append        

    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        img_url = urljoin(url, link)
        url_list.append(img_url)
    
    for raw_img in soup.find_all("link"):
        link = raw_img.get("href")
        is_image = any(map(lambda ext: ext in link,image_extensions)) # true if any of the extensions is contained within the url
        if is_image:
            img_url = urljoin(url, link)
            url_list.append(img_url)


        
    
    # base case, if we've reached max depth then don't go to children
    if current_depth == max_depth:
        return url_list
    
    # for each anchor in the page,get the absolute url and scrape that page for images
    for anchor in soup.find_all('a'):
        link = anchor.get("href")
        child_url = urljoin(url, link)
        child_list = recursively_scrape(child_url, current_depth+1,max_depth)
        if current_depth == 1:
            application.logger.info("Collected " + str(len(child_list)) + " image urls from: " + child_url)

        url_list.extend(child_list) # merge the children list with the current list

    
    

    return list(dict.fromkeys(url_list)) # remove duplicates


