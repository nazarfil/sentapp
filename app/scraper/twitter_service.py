import requests, time

BT = "AAAAAAAAAAAAAAAAAAAAAEL3MgEAAAAA9YRG3JcE3J1UEr9ZgV4Acvpxe7A%3DuPoXPrxf1VFGtpeIxgWPq4i36YrTUfHrwqMEyG4Te5YBLj3Lf7"
url_for_recent_tweets = "https://api.twitter.com/2/tweets/search/recent?query={}&{}"


# define search twitter function
def search_twitter(query, **kwargs):
    global response
    headers = {"Authorization": "Bearer {}".format(BT)}
    tweet_fields = "tweet.fields=text,author_id,created_at"
    url = url_for_recent_tweets.format(query, tweet_fields)
    for key, value in kwargs.items():
        url = url + "&{}={}".format(key, value)
    status_code = 429
    while status_code != 200:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 429 or response.status_code == 400:
            time.sleep(180)
        status_code =response.status_code
        print(response.status_code)
    return response.json()
