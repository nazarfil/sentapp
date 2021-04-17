import unittest

from app.database.models import InputData
from app.scraper.twitter.search_tweets_for_input import build_tweet_query


class TestTwitterScrapeJob(unittest.TestCase):
    def testBuildTwitterQuery(self):
        iin_data = InputData(name="Bitcoin", source="twit", date="2021-04-21", ticker="BTC", order=3, string_id="bitcoin")
        query="(Bitcoin or #BTC or $BTC) and -is:retweet"
        query_result =  build_tweet_query(iin_data)
        self.assertEqual(query, query_result)
