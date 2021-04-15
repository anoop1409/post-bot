import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from posts import get_all_filtered_posts
from settings import (
    LINKEDIN_LOGIN_URL,
    LINKEDIN_POSTS_URL,
    LINKEDIN_PASSWORD,
    LINKEDIN_USERNAME,
    SCRAPE_MODE_HEADLESS,
    DISCORD_CHANNEL_BOT_USERNAME,
    DISCORD_CHANNEL_WEBHOOK_URL,
)


logging.info("Setting up selenium")
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1600,800")

if SCRAPE_MODE_HEADLESS:
    logging.info("Running selenium in headless mode")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

browser = webdriver.Chrome(options=options)

logging.info("Open login page")
browser.get(LINKEDIN_LOGIN_URL)

logging.info("Enter credentials")
elementID = browser.find_element_by_id("username")
elementID.send_keys(LINKEDIN_USERNAME)

logging.info("Submit login form")
elementID = browser.find_element_by_id("password")
elementID.send_keys(LINKEDIN_PASSWORD)
elementID.submit()

logging.info("Opening the posts page for a given user")
browser.get(LINKEDIN_POSTS_URL)
time.sleep(5)

logging.info("Initializing BS4")
src = browser.page_source
soup = BeautifulSoup(src, "lxml")

logging.info("Looping over the found posts")
for user_post in get_all_filtered_posts(soup, browser):
    values = {"username": DISCORD_CHANNEL_BOT_USERNAME, "content": user_post}

    logging.info("Posting to Discord channel")
    response = requests.post(
        DISCORD_CHANNEL_WEBHOOK_URL,
        json=values,
        headers={"Content-Type": "application/json"},
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(err)
    else:
        logging.info(f"Payload delivered successfully {response.status_code}")
