import requests
from app import log, Config

url_for_recent_tweets = "https://api.twitter.com/2/tweets/search/recent?query={}&{}"
logger = log.setup_custom_logger('scraper')

config = Config()


# define search twitter function
def search_twitter(query, **kwargs):
    response = {}
    max_calls = 3
    headers = {"Authorization": "Bearer {}".format(config.TWITTER_TOKEN)}
    fields_to_return = "tweet.fields=public_metrics,id,text,author_id,created_at&expansions=author_id&user.fields=public_metrics,id"
    url = url_for_recent_tweets.format(query, fields_to_return)
    for key, value in kwargs.items():
        url = url + "&{}={}".format(key, str(value))
    status_code = 429
    logger.debug("Calling twitter with request {}".format(url))
    calls_count = 0
    try:
        while status_code != 200 and calls_count < max_calls:
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 429 or response.status_code == 400:
                logger.debug("Calling twitter resulted in : {}".format(response.status_code))
            status_code = response.status_code
            calls_count += 1
    except:
        return {}
    try:
        response = response.json()
    except:
        return {}

    return response
