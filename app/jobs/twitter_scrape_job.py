import csv
import datetime

from app import log
from app.jobs.calculate_hype_score_job import calculate_hype_score
from app.jobs.populate_price_job import create_financial_record_for_coins
from app.jobs.populate_sentiment_for_input_job import calculate_sentiment_for_tweet
from app.scraper.twitter.search_tweets_for_input import get_tweet_for_input, get_tweets_for_range, format_T_H_M_S_ZZ
from app.database.models import ScrapedData, InputData, TwitterDataMetric, db

from app.services import database_service
from app.utility.formats import foramt_Y_M_D

MAX_TWEETS = 400
logger = log.setup_custom_logger('jobs')


def scrape_twitter_from_db(date):
    coins = InputData.query.all()
    if coins is None:
        pass
    for coin in coins:
        calculate_score_for_tweet(coin, date)


def scrape_twitter_from_db_range():
    coins = InputData.query.all()
    logger.info("Calculating score for" + str(len(coins)))
    now = datetime.datetime.utcnow()
    back_15min = now - datetime.timedelta(minutes=15)
    back_30min = now - datetime.timedelta(minutes=30)
    start_date = back_30min.strftime(format_T_H_M_S_ZZ) + 'Z'
    end_date = back_15min.strftime(format_T_H_M_S_ZZ) + 'Z'
    date_str = back_15min.strftime(foramt_Y_M_D)

    for coin in coins:
        logger.info("Calculating score for {} ".format(coin.name))
        calculate_score_for_tweet_range(coin, start_date, end_date)
        calculate_hype_score(date_str, input_data_id=coin.id)

    create_financial_record_for_coins(coins, date_str)


def scrape_twitter_from_db_coin(name, date):
    coin = InputData.query.filter_by(name=name).first()
    if coin is None:
        pass
    calculate_score_for_tweet(coin, date)


def calculate_score_for_tweet_range(coin, start_date, end_date, token="none"):
    logger.info("Calculating score for {} ".format(coin.name))
    tweets = get_tweets_for_range(coin, start_date, end_date, next_token=token)
    try:
        if tweets["meta"]["result_count"] > 0:
            tweets_records = create_scraped_data_records(tweets, coin)
            for tr in tweets_records:
                calculate_sentiment_for_tweet(coin, tr)
            there_is_next_token = "next_token" in tweets["meta"]
            if there_is_next_token:
                token = tweets["meta"]["next_token"]
                calculate_score_for_tweet_range(coin, start_date, end_date, token)
    except:
        logger.error("No results for " + str(coin.name))


def calculate_score_for_tweet(coin, date, token="none"):
    logger.info("Calculating score for {} ".format(coin.name))
    tweets = get_tweet_for_input(coin, input_date=date, next_token=token)
    try:
        if tweets["meta"]["result_count"] > 0:
            tweets_records = create_scraped_data_records(tweets, coin)
            for tr in tweets_records:
                calculate_sentiment_for_tweet(coin, tr)
            there_is_next_token = "next_token" in tweets["meta"]
            if there_is_next_token:
                token = tweets["meta"]["next_token"]
                calculate_score_for_tweet(coin, date, token)
    except:
        logger.error("No results for " + str(coin.name))


def create_scraped_data_record(tweets, input_data):
    source = "twitter"
    logger.info("Adding record with  {} from {}".format(input_data.id, source))
    for tweet in tweets["data"]:
        text_data = tweet["text"]
        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))
        if len(text_data) > 260:
            text_data = text_data[0:260]
        database_service.create_and_save_scrape_data(input_data, source, text_data, tweet)


def create_scraped_data_records(tweets, coin):
    source = "twitter"
    logger.info("Adding record with {} from {} ".format(coin.id, source))
    tweets_list = []
    users = tweets["includes"]["users"]
    for tweet in tweets["data"]:
        text_data = tweet["text"]
        author_id = tweet["author_id"]
        metric = tweet["public_metrics"]

        user = find_user(users, author_id)
        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))

        if len(text_data) > 260:
            text_data = text_data[0:260]

        scraped_record = ScrapedData(text=text_data,
                                     date=tweet["created_at"],
                                     source=source,
                                     source_id=tweet["id"],
                                     input_data=coin.id)
        db.session.add(scraped_record)
        db.session.commit()
        
        twitter_metric = TwitterDataMetric(
            scraped_data=scraped_record.id,
            followers=user["public_metrics"]["followers_count"],
            retweet=metric["retweet_count"],
            replies=metric["reply_count"],
            likes=metric["like_count"],
            quotes=metric["quote_count"]
        )
        db.session.add(twitter_metric)
        db.session.commit()
        tweets_list.append(scraped_record)
    return tweets_list


def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user
