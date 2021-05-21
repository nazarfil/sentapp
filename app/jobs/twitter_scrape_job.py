import datetime

from app.jobs.calculate_hype_score_job import calculate_hype_score
from app.jobs.populate_price_job import create_financial_record_for_coins
from app.jobs.update_database import update_order
from app.scraper.twitter.search_tweets_for_input import get_tweet_for_input, get_tweets_for_range, format_T_H_M_S_ZZ
from app.database.models import TwitterData, InputData, db, SentimentScore
from app.algos.sentiment_aws import AwsClient

from app.utility.formats import foramt_Y_M_D


import app.log as log
logger = log.def_logger


class TwitterJob(object):
    """
    This is a job to scrape twitter and create scraped ata entries to db
    """

    def __init__(self):
        self.MAX_TWEETS = 4
        self.MAX_TWEETS_ALL = 2
        self.MAX_POOL_REQUEST = 450

    def scrape_twitter_from_db(self, date):
        """
        :param date: date to scrape twitter on (should be in range of last 7 days)
        :type date: str
        """
        coins = InputData.query.all()
        if coins is None:
            pass
        for coin in coins:
            self.calculate_score_for_tweet(coin, date, called=0)

    def scrape_twitter_from_db_range(self):
        """
        Scraping twitter for last 30 min, create tweet, metric, financial and score data
        :rtype: void
        """
        coins = InputData.query.all()
        now = datetime.datetime.utcnow()
        back_30min = now - datetime.timedelta(minutes=30)
        back_60min = now - datetime.timedelta(minutes=60)
        start_date = back_60min.strftime(format_T_H_M_S_ZZ) + 'Z'
        end_date = back_30min.strftime(format_T_H_M_S_ZZ) + 'Z'
        date_str = back_30min.strftime(foramt_Y_M_D)

        for coin in coins:
            logger.info("Calculating score for {} ".format(coin.name))
            try:
                self.calculate_score_for_tweet_range(coin=coin, start_date=start_date, end_date=end_date, called=0)
                calculate_hype_score(date_str, input_data_id=coin.id)
            except Exception as e:
                logger.error("Error creating score for coin {}".format(str(coin.name)))
                logger.error(e)

        create_financial_record_for_coins(coins, date_str)
        update_order()

    def scrape_twitter_from_db_coin(self, name, date):
        """
        Scrapes twitter
        :param name: name of the coin
        :type name: str
        :param date: date to scrape
        :type date: str
        """
        coin = InputData.query.filter_by(name=name).first()
        if coin is None:
            pass
        self.calculate_score_for_tweet(coin, date, called=0)

    def calculate_score_for_tweet_range(self, coin, start_date, end_date, called=0, token="none"):
        """
        Recursive method to get tweets and calculate sentiment score for tweets in datetime range
        :param coin: coin name to calculate score for
        :type coin: str
        :param start_date: start date
        :type start_date: datetime
        :param end_date: end date
        :type end_date: datetime
        :param called: how many times twitter was called
        :type called: int
        :param token: twitter token for next
        :type token: str
        """

        called = called + 1
        tweets = get_tweets_for_range(coin, start_date, end_date, next_token=token)
        if tweets is not None and "meta" in tweets:
            if tweets["meta"]["result_count"] > 0:
                tweets_records = self.create_scraped_data_records(tweets, coin)
                for tr in tweets_records:
                    self.calculate_sentiment_for_tweet(coin, tr)
                there_is_next_token = "next_token" in tweets["meta"]
                if there_is_next_token and called < self.MAX_TWEETS:
                    token = tweets["meta"]["next_token"]
                    self.calculate_score_for_tweet_range(coin, start_date, end_date, called, token)

    def calculate_score_for_tweet(self, coin, date, called, token="none"):
        """
        Recursive method to get tweets and calculate sentiment score for tweets in date range
        :param coin: coin name to calculate score for
        :type coin: str
        :param date: date to scrape for
        :type date: str date
        :param token: twitter token for next
        :type token: str
        """
        logger.info("Calculating score for {} ".format(coin.name))
        tweets = get_tweet_for_input(coin, input_date=date, next_token=token)
        try:
            if tweets["meta"]["result_count"] > 0:
                tweets_records = self.create_scraped_data_records(tweets, coin)
                for tr in tweets_records:
                    self.calculate_sentiment_for_tweet(coin, tr)
                there_is_next_token = "next_token" in tweets["meta"]
                if there_is_next_token and called < self.MAX_TWEETS_ALL:
                    token = tweets["meta"]["next_token"]
                    self.calculate_score_for_tweet(coin, date, called + 1, token)
        except:
            logger.error("No results for " + str(coin.name))

    def create_scraped_data_records(self, tweets, coin):
        """
        Creating records in db for scraped tweets and its metric, returns the created tweet records
        :param tweets: tweets returned from twitter
        :type tweets: dict
        :param coin: coin record
        :type coin: object
        :return: list of scraped tweet records
        :rtype: list
        """
        tweets_list = []
        users = tweets["includes"]["users"]
        for tweet in tweets["data"]:
            scraped_record = self.create_scraped_data_from_twitter(tweet, users, coin_id=coin.id)
            db.session.add(scraped_record)
            db.session.commit()
        return tweets_list

    def calculate_sentiment_for_tweet(self, coin, tweet, client=AwsClient()):
        """

        :param coin:
        :param tweet:
        :param client:
        :return:
        """
        sentiment = client.get_sentiment(text=tweet.text)
        self.assign_score(coin, tweet, sentiment, client.name)

    def create_scraped_data_from_twitter(self, tweet, users, coin_id) -> object:
        """
        Creates record form tweets scraped
        :param tweet: tweet dictionary
        :type tweet: dict
        :param coin_id: coin id
        :type coin_id: int
        :return: tweet record object
        :rtype: object
        """
        source = "twitter"
        text_data = tweet["text"]

        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))

        if len(text_data) > 260:
            text_data = text_data[0:260]

        author_id = tweet["author_id"]
        user = self.find_user(users, author_id)
        metric = tweet["public_metrics"]
        return TwitterData(text=text_data,
                           date=tweet["created_at"],
                           source=source,
                           source_id=tweet["id"],
                           input_data=coin_id,
                           followers=user["public_metrics"]["followers_count"],
                           retweet=metric["retweet_count"],
                           replies=metric["reply_count"],
                           likes=metric["like_count"],
                           quotes=metric["quote_count"])

    @staticmethod
    def find_user(users, user_id):
        """
        Find the user object in a list based on userid
        :param users: list of users
        :type users: list
        :param user_id:
        :type user_id: str
        :return: user form the list
        :rtype: object
        """
        for user in users:
            if user["id"] == user_id:
                return user

    def assign_score(self, input_data, tweet, sentiment, source):
        """

        :param input_data:
        :param date:
        :param sentiment:
        :param source:
        :return:
        """
        sentiment_record = SentimentScore(
            input_data=input_data.id,
            twitter_data_id = tweet.id,
            sentiment=sentiment["Sentiment"],
            positive=sentiment["SentimentScore"]["Positive"],
            negative=sentiment["SentimentScore"]["Negative"],
            neutral=sentiment["SentimentScore"]["Neutral"],
            mixed=sentiment["SentimentScore"]["Mixed"],
            date=tweet.date,
            source=source

        )
        db.session.add(sentiment_record)
        db.session.commit()
