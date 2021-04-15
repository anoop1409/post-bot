import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

from scraper.settings import POSTS_SEARCH_TERMS


def get_all_filtered_posts(soup: BeautifulSoup, browser: webdriver.Chrome):
    units_of_time = ["second", "minute", "hour"]
    filtered_posts = []
    search_term_array = POSTS_SEARCH_TERMS.split(",")
    posts = soup.findAll("div", attrs={"class": "occludable-update"})

    for post in posts:
        feed = post.find("span", class_="feed-shared-actor__sub-description")

        if feed is not None:
            relative_publish_time_text = feed.find("span", class_="visually-hidden")
            post_content = post.find("span", class_="break-words")

            # Posts do not have a timestamp section; It contain text stating when a post was published
            # Text is relative to current time. Examples include 1 hour ago, 20 hours ago, 2 days ago etc.
            # Filtering posts which have 'second', 'minute', 'hour' in text, to get only new posts
            # In addition to this, posts are filtered based on the post search terms
            if any(
                unit in relative_publish_time_text.text for unit in units_of_time
            ) and any(
                post_content.find(text=re.compile(search_term, re.IGNORECASE))
                for search_term in search_term_array
            ):

                # Click on the button to open the post sharing menu
                button = browser.find_element_by_class_name(
                    "feed-shared-control-menu__trigger"
                )
                button.click()
                time.sleep(1)

                # Click on the option to 'Copy link to post'
                button = browser.find_element_by_xpath(
                    '//*[text()="Copy link to post"]'
                )
                button.click()
                time.sleep(1)

                # Copy the post url and append to the post content
                link = browser.find_element_by_class_name(
                    "artdeco-toast-item__cta"
                ).get_attribute("href")
                post_data = post_content.get_text() + link
                filtered_posts.append(post_data)

    return filtered_posts
