from selenium import webdriver
from bs4 import BeautifulSoup
import re

#Import configuration data
from settings import LINKEDIN_USERNAME,LINKEDIN_PASSWORD,LINKEDIN_LOGIN_URL,LINKEDIN_POSTS_URL,POSTS_SEARCH_TERMS,CHROME_DRIVER_PATH

#Initialize Selenium web driver for Chrome
browser = webdriver.Chrome(CHROME_DRIVER_PATH)

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

#Search terms list
searchTermArray = POSTS_SEARCH_TERMS.split(',')

#Looping over posts
###Todo filter posts based on current days timestamp
for posts in soup.find_all('span',class_="break-words"):
    for searchTerm in searchTermArray:
        if posts.find(text=re.compile(searchTerm)):
            print(searchTerm, posts.get_text())
    

