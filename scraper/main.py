import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import discord
import requests
import time

# Import configuration data
from settings import (LINKEDIN_LOGIN_URL, LINKEDIN_POSTS_URL, LINKEDIN_PASSWORD, LINKEDIN_USERNAME,
                      SCRAPE_MODE_HEADLESS, POSTS_SEARCH_TERMS, DISCORD_CHANNEL_BOT_USERNAME, DISCORD_CHANNEL_WEBHOOK_URL)

# Initialize Selenium web driver for Chrome
options = Options()
options.add_argument('--window-size=1600,800')

# Running selenium in headless mode if SCRAPE_MODE_HEADLESS is true
if SCRAPE_MODE_HEADLESS:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

# Set chromedriver location in PATH
browser = webdriver.Chrome(options=options)

# Open login page
browser.get(LINKEDIN_LOGIN_URL)

# Enter login info:
elementID = browser.find_element_by_id('username')
elementID.send_keys(LINKEDIN_USERNAME)

elementID = browser.find_element_by_id('password')
elementID.send_keys(LINKEDIN_PASSWORD)

elementID.submit()

# Open posts page for a given user
browser.get(LINKEDIN_POSTS_URL)
time.sleep(5)

# BS4 setup for posts page
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')

units_of_time = ['second', 'minute', 'hour']

# Search terms list
search_term_array = POSTS_SEARCH_TERMS.split(',')


def get_all_filtered_posts():
    posts = soup.findAll('div', attrs={'class': 'occludable-update'})

    filtered_posts = []

    for post in posts:
        feed = post.find('span', class_='feed-shared-actor__sub-description')

        if feed is not None:
            relative_publish_time_text = feed.find(
                'span', class_='visually-hidden')
            post_content = post.find('span', class_='break-words')

            # Posts do not have a timestamp section; It contain text stating when a post was published
            # Text is relative to current time. Examples include 1 hour ago, 20 hours ago, 2 days ago etc.
            # Filtering posts which have 'second', 'minute', 'hour' in text, to get only new posts
            # In addition to this, posts are filtered based on the post search terms
            if any(unit in relative_publish_time_text.text for unit in units_of_time) and any(post_content.find(text=re.compile(search_term, re.IGNORECASE)) for search_term in search_term_array):

                # Click on the button to open the post sharing menu
                button = browser.find_element_by_class_name(
                    'feed-shared-control-menu__trigger')
                button.click()
                time.sleep(1)

                # Click on the option to 'Copy link to post'
                button = browser.find_element_by_xpath(
                    '//*[text()="Copy link to post"]')
                button.click()
                time.sleep(1)

                # Copy the post url and append to the post content
                link = browser.find_element_by_class_name(
                    'artdeco-toast-item__cta').get_attribute('href')
                post_data = post_content.get_text()+link
                filtered_posts.append(post_data)
    return filtered_posts


# Looping over the posts which are filtered based on current day and the search terms
# Delivering the posts to the discord channel via web hook api
for user_post in get_all_filtered_posts():
    values = {
        "username": DISCORD_CHANNEL_BOT_USERNAME,
        "content": user_post
    }

    response = requests.post(
        DISCORD_CHANNEL_WEBHOOK_URL, json=values,
        headers={'Content-Type': 'application/json'}
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print('Payload delivered successfully, code {}.'.format(
            response.status_code))
