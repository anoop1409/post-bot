from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import re

#Import configuration data
import settings

#Initialize Selenium web driver for Chrome
options = Options()

# Running selenium in headless mode if SCRAPE_MODE_HEADLESS is true
if(settings.SCRAPE_MODE_HEADLESS == 'true'):
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

# Set chromedriver location in PATH
browser = webdriver.Chrome(options=options)

#Open login page
browser.get(settings.LINKEDIN_LOGIN_URL)

#Enter login info:
elementID = browser.find_element_by_id('username')
elementID.send_keys(settings.LINKEDIN_USERNAME)

elementID = browser.find_element_by_id('password')
elementID.send_keys(settings.LINKEDIN_PASSWORD)

elementID.submit()

#Open posts page for a given user
browser.get(settings.LINKEDIN_POSTS_URL)

#BS4 setup for posts page
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

units_of_time = ["second","minute","hour"]
def get_all_posts():
    posts = soup.find_all('div',class_="occludable-update")
    filtered_posts = []
    for post in posts:
        feed = post.find('span',class_="feed-shared-actor__sub-description")
       
        if (feed != None):
            relative_publish_time_text = feed.find('span',class_="visually-hidden")
            
            # Posts do not have a timestamp section; It contain text stating when a post was published
            # Text is relative to current time. Examples include 1 hour ago, 20 hours ago, 2 days ago etc.
            # Filtering posts which have 'hour' in text, to get only new posts
            if any(unit in relative_publish_time_text.text for unit in units_of_time):
                filtered_posts.append(post.find('span',class_="break-words"))
    return filtered_posts

def filter_posts(posts,search_term):
    return posts.find(text=re.compile(search_term, re.IGNORECASE))

#Search terms list
search_term_array = settings.POSTS_SEARCH_TERMS.split(',')

all_user_posts = get_all_posts()

#Looping over posts
for posts in all_user_posts:
    for search_term in search_term_array:
        if filter_posts(posts,search_term):
            print(search_term, posts.get_text())
