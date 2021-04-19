import requests
import time
import re

messari_assets = "https://data.messari.io/api/v2/assets/{}/profile"


def get_assets(name):
    global response
    url = messari_assets.format(name)
    status_code = 429
    while status_code != 200:
        response = requests.request("GET", url)
        if response.status_code == 429 or response.status_code == 400:
            time.sleep(180)
        status_code = response.status_code
    return response.json()


def get_messari_description(name):
    profile = get_assets(name)
    if "error_code" not in profile['status']:
        data = profile["data"]["profile"]
        raw_desc = data["general"]["overview"]["project_details"]
        filtered_desc = re.sub(r'<.+?>', ' ', raw_desc)
        return filtered_desc
    else:
        return "NOT_AVAILABLE"
