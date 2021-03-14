from datetime import time
from os import environ
from datetime import datetime
import requests

from app import log

cc_endpoint = "https://min-api.cryptocompare.com/data/v2/histoday"
query_price = "?fsym={}&tsym={}&limit={}&toTs={}"
auth_header = "Apikey"
auth_header_value = environ.get("CRYPTOCOMPARE_TOKEN")

logger = log.setup_custom_logger('scraper')


def get_historical_data(coin, currency='USD', limit=10, to_date=datetime.now().timestamp()):
    global response
    headers = {auth_header: auth_header_value}
    query = query_price.format(coin, currency, limit, to_date)
    url = cc_endpoint + query
    status_code = 429
    logger.debug("Calling CryptoCompare with request {}".format(url))
    while status_code != 200:
        response = requests.request("GET", url, headers=headers)
        logger.debug("Calling CryptoCompare resulted in : {}".format(response.status_code))
        if response.status_code == 429 or response.status_code == 400:
            time.sleep(180)
        status_code = response.status_code
    return response.json()
