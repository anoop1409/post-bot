from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import re

#Import configuration data
from settings import LINKEDIN_USERNAME,LINKEDIN_PASSWORD,LINKEDIN_LOGIN_URL,LINKEDIN_POSTS_URL,POSTS_SEARCH_TERMS,CHROME_DRIVER_PATH,TEST_MODE_HEADLESS

#Initialize Selenium web driver for Chrome
options = Options()

# Running selenium in headless mode if TEST_MODE_HEADLESS is true
if(TEST_MODE_HEADLESS == 'true'):
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
browser = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)

#Open login page
browser.get(LINKEDIN_LOGIN_URL)

#Enter login info:
elementID = browser.find_element_by_id('username')
elementID.send_keys(LINKEDIN_USERNAME)

elementID = browser.find_element_by_id('password')
elementID.send_keys(LINKEDIN_PASSWORD)

elementID.submit()

#Open posts page for a given user
browser.get(LINKEDIN_POSTS_URL)

#BS4 setup for posts page
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

def getAllPosts():
    posts = soup.find_all('div',class_="occludable-update")
    filteredPosts = []
    for post in posts:
        feed = post.find('span',class_="feed-shared-actor__sub-description")
       
        if (feed != None):
            relativePublishTimeText = feed.find('span',class_="visually-hidden")
            
            # Posts do not have a timestamp section; It contain text stating when a post was published
            # Text is relative to current time. Examples include 1 hour ago, 20 hours ago, 2 days ago etc.
            # Filtering posts which have 'hour' in text, to get only new posts
            if("hour" in relativePublishTimeText.text):
                filteredPosts.append(post.find('span',class_="break-words"))
    return filteredPosts

def filterPosts(posts,searchTerm):
    return posts.find(text=re.compile(searchTerm, re.IGNORECASE))

#Search terms list
searchTermArray = POSTS_SEARCH_TERMS.split(',')

allUserPosts = getAllPosts()

#Looping over posts
for posts in allUserPosts:
    for searchTerm in searchTermArray:
        if filterPosts(posts,searchTerm):
            print(searchTerm, posts.get_text())
