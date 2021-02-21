import requests
BT = "AAAAAAAAAAAAAAAAAAAAAEL3MgEAAAAA9YRG3JcE3J1UEr9ZgV4Acvpxe7A%3DuPoXPrxf1VFGtpeIxgWPq4i36YrTUfHrwqMEyG4Te5YBLj3Lf7"
url_for_recent_tweets = "https://api.twitter.com/2/tweets/search/recent?query={}&{}"


# define search twitter function
def search_twitter(query, **kwargs):
    headers = {"Authorization": "Bearer {}".format(BT)}
    tweet_fields = "tweet.fields=text,author_id,created_at"
    url = url_for_recent_tweets.format(query, tweet_fields)
    for key, value in kwargs.items():
        url = url + "&{}={}".format(key, value)
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
