import requests, time
from os import environ, path
from app import log

url_for_recent_tweets = "https://api.twitter.com/2/tweets/search/recent?query={}&{}"
BT = environ.get("TWITTER_TOKEN")

logger = log.setup_custom_logger('scraper')


# define search twitter function
def search_twitter(query, **kwargs):
    global response
    headers = {"Authorization": "Bearer {}".format(BT)}
    fields_to_return = "tweet.fields=text,author_id,created_at"
    url = url_for_recent_tweets.format(query, fields_to_return)
    for key, value in kwargs.items():
        url = url + "&{}={}".format(key, str(value))
    status_code = 429
    logger.debug("Calling twitter with request {}".format(url))
    while status_code != 200:
        response = requests.request("GET", url, headers=headers)
        logger.debug("Calling twitter resulted in : {}".format(response.status_code))
        if response.status_code == 429 or response.status_code == 400:
            time.sleep(180)
        status_code = response.status_code
    return response.json()