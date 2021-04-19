import unittest
import re
from app.scraper.messari.messari_scraper import get_assets


class TestTwitterScrapeJob(unittest.TestCase):
    asset = "Bitcoin"
    profile = get_assets(asset)
    if "error_code" not in profile['status']:
        data = profile["data"]["profile"]
        raw_desc = data ["general"]["overview"]["project_details"]
        #filtered_desc = raw_desc.
        filtered_desc = re.sub(r'<.+?>', ' ',raw_desc)
        print(filtered_desc)
