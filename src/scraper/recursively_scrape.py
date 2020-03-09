import requests
import re
from bs4 import BeautifulSoup


image_extensions = ['.png', '.gif', '.jpg', '.svg']
def recursively_scrape(url, current_depth=0, max_depth=2):
    '''
    NOT COMPLETE
    '''

    if current_depth == max_depth:
        return

    html = requests.get(url).text # basic "scraper" right now
    
    
    soup = BeautifulSoup(html, 'html.parser')
    url_list = []

    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        url_list.append(link)

    return url_list


#print(recursively_scrape("http://4chan.org/"))