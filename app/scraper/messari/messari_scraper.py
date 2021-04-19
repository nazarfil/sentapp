import requests
import time
import re

messari_assets = "https://data.messari.io/api/v2/assets/{}/profile"


def get_assets(name):
    global response
    url = messari_assets.format(name)
    response = requests.request("GET", url)
    return response.json()


def get_messari_description(name):
    profile = get_assets(name)
    print(name)
    if "error_code" not in profile['status']:
        try:
            data = profile["data"]["profile"]
            raw_desc = data["general"]["overview"]["project_details"]
            filtered_desc = re.sub(r'<.+?>', ' ', raw_desc)
            return filtered_desc
        except:
            return "NOT_AVAILABLE"
    else:
        return "NOT_AVAILABLE"
