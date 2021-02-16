import requests
import json

class TwitterScraper:
    BT="AAAAAAAAAAAAAAAAAAAAAEL3MgEAAAAA9YRG3JcE3J1UEr9ZgV4Acvpxe7A%3DuPoXPrxf1VFGtpeIxgWPq4i36YrTUfHrwqMEyG4Te5YBLj3Lf7"
    uri='https://api.twitter.com/1.1/search/tweets.json?q=%23bitcoin%20and%20%23btc&lang=en&result_type=recent'
    #define search twitter function
    def search_twitter(query, tweet_fields, bearer_token = BT):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
            query, tweet_fields
        )
        response = requests.request("GET", url, headers=headers)

        print(response.status_code)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()