import csv
import datetime

from app import log
from app.jobs.calculate_hype_score_job import calculate_hype_score
from app.jobs.populate_price_job import create_financial_record_for_coins
from app.jobs.populate_sentiment_for_input_job import calculate_sentiment_for_tweet
from app.scraper.twitter.search_tweets_for_input import get_tweet_for_input, get_tweets_for_range, format_T_H_M_S_ZZ
from app.database.models import ScrapedData, InputData, TwitterDataMetric, db

from app.utility.formats import foramt_Y_M_D

MAX_TWEETS = 5
logger = log.setup_custom_logger('jobs')


def scrape_twitter_from_db(date):
    coins = InputData.query.all()
    if coins is None:
        pass
    for coin in coins:
        calculate_score_for_tweet(coin, date)


def scrape_twitter_from_db_range():
    coins = InputData.query.all()
    #logger.info("Calculating score for" + str(len(coins)))
    now = datetime.datetime.utcnow()
    back_15min = now - datetime.timedelta(minutes=15)
    back_30min = now - datetime.timedelta(minutes=30)
    start_date = back_30min.strftime(format_T_H_M_S_ZZ) + 'Z'
    end_date = back_15min.strftime(format_T_H_M_S_ZZ) + 'Z'
    date_str = back_15min.strftime(foramt_Y_M_D)

    for coin in coins:
        logger.info("Calculating score for {} ".format(coin.name))
        try:
            calculate_score_for_tweet_range(coin, start_date, end_date, 0)
            calculate_hype_score(date_str, input_data_id=coin.id)
        except:
            logger.error("Error creating score for coin {}".format(str(coin.name)))

    create_financial_record_for_coins(coins, date_str)


def scrape_twitter_from_db_coin(name, date):
    coin = InputData.query.filter_by(name=name).first()
    if coin is None:
        pass
    calculate_score_for_tweet(coin, date)


def calculate_score_for_tweet_range(coin, start_date, end_date, called, token="none"):
    tweets = get_tweets_for_range(coin, start_date, end_date, next_token=token)
    if tweets is not None and "meta" in tweets:
        if tweets["meta"]["result_count"] > 0:
            tweets_records = create_scraped_data_records(tweets, coin)
            for tr in tweets_records:
                calculate_sentiment_for_tweet(coin, tr)
            there_is_next_token = "next_token" in tweets["meta"]
            if there_is_next_token and called < MAX_TWEETS:
                token = tweets["meta"]["next_token"]
                calculate_score_for_tweet_range(coin, start_date, end_date,called+1, token)


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


def create_scraped_data_records(tweets, coin):
    tweets_list = []
    users = tweets["includes"]["users"]
    for tweet in tweets["data"]:
        scraped_record = create_scraped_data_from_twitter(tweet, coin_id=coin.id)
        db.session.add(scraped_record)
        db.session.commit()

        twitter_metric = create_metric_data(tweet, users, scraped_record_id=scraped_record.id)
        db.session.add(twitter_metric)
        tweets_list.append(scraped_record)
        db.session.commit()

    return tweets_list


def find_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user


def create_metric_data(tweet, users, scraped_record_id):
    author_id = tweet["author_id"]
    user = find_user(users, author_id)
    metric = tweet["public_metrics"]
    return TwitterDataMetric(
        scraped_data=scraped_record_id,
        followers=user["public_metrics"]["followers_count"],
        retweet=metric["retweet_count"],
        replies=metric["reply_count"],
        likes=metric["like_count"],
        quotes=metric["quote_count"]
    )


def create_scraped_data_from_twitter(tweet, coin_id) -> object:
    source = "twitter"
    text_data = tweet["text"]

    text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))

    if len(text_data) > 260:
        text_data = text_data[0:260]
    return ScrapedData(text=text_data,
                       date=tweet["created_at"],
                       source=source,
                       source_id=tweet["id"],
                       input_data=coin_id)
