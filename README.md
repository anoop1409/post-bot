# Post-bot

A LinkedIn post scraping bot

## Introduction

- This bot can scrape posts published by a particular user on LinkedIn. The user should be your first level connection or their posts should be public.

- The `settings.py` file can be updated to enter the username whose posts should be scraped.

- A specific keyword or a list of keywords can be specified inside the `settings.py`. These keywords will be used to filter the posts for scraping.

- Only new posts will be fetched and notified to a `Discord` channel with a link to the post.

## Web Scraping

To run the python script for web scraping, navigate to the `scraper` folder and follow the below given steps:

1. Make sure chrome driver path is added to `PATH` environment variable

2. Rename `sample-settings.py` file to `settings.py`

3. Within `settings.py`, enter credentials for the LinkedIn account which will be used for scraping. Also enter the user who's posts have to be scraped and the search terms.

4. Once the above changes are done, run `python3 main.py` from inside the `scraper` folder path.

5. To run selenium in non-headless mode, make the following changes in `settings.py` file: 
    ```
    SCRAPE_MODE_HEADLESS = False
    ```
