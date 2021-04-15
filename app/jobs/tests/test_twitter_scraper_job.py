import unittest

from app.jobs.resources.test_data import twitter_resp
from app.jobs.twitter_scrape_job import create_metric_data, create_scraped_data_from_twitter


class TestTwitterScrapeJob(unittest.TestCase):
    tweets = twitter_resp

    def testCreateRecordFromTwitter(self):
        tweet = self.tweets["data"][0]
        coin_id = 1
        record = create_scraped_data_from_twitter(tweet, coin_id)
        self.assertIsNotNone(record)

    def testCreateMetricFromTweet(self):
        tweet = self.tweets["data"][0]
        coin_id = 1
        record = create_scraped_data_from_twitter(tweet, coin_id)

        users = self.tweets["includes"]["users"]
        metric = create_metric_data(tweet, users=users, scraped_record_id=record.id)
        self.assertIsNotNone(metric)