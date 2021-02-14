# post-bot

A LinkedIn post scraping bot

## Introduction

- This bot can scrape posts published by a particular user on LinkedIn. The user should be your first level connection or their posts should be public.
- The settings.py file can be updated to enter the username whose posts should be scraped.
- A specific keyword or a list of keywords can be specified inside the settings.py. These keywords will be used to filter the posts for scraping.
- Only new posts should be fetched and notified to a `Discord` channel with a link to the post (If possible).

## Web Scraping

To run the python script for web scraping, navigate to the web-scraper folder and follow the below given steps:

- Make sure chrome driver path is added to PATH environment variable
- Rename sample-settings.py file to settings.py
- Within settings.py, enter credentials for the LinkedIn account which will to be used for scraping. Also enter the user who's posts have to be scraped and the search terms. Sample values:

`LINKEDIN_USERNAME = 'test-email@testtest.com'`  
`LINKEDIN_PASSWORD = 'testpassword'`  
`LINKEDIN_POSTS_URL = 'https://www.linkedin.com/in/dummy-user/detail/recent-activity/shares/'`  
`POSTS_SEARCH_TERMS = 'Python,Django'`

- Once the above changes are done, run python3 index.py from inside the web-scraper folder path. The posts which satisfy the given criteria of search terms for the given user, will be printed in the terminal.

- To run selenium in headless mode, make the following changes in settings.py file `SCRAPE_MODE_HEADLESS = 'true'` otherwise make this as `false`
