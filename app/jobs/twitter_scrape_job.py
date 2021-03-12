import csv

from app.jobs.populate_sentiment_for_input_job import calculate_sentiment_for_tweet
from app.scraper.twitter.search_tweets_for_input import get_tweet_for_input
from app.database.models import ScrapedData, InputData
import logging

from app.services import database_service

MAX_TWEETS = 400


def scrape_twitter_from_db(date):
    coins = InputData.query.all()
    if coins is None:
        pass
    for coin in coins:
        calculate_score_for_tweet(coin, date)
        calculate_score_for_tweet(coin, date)


def scrape_twitter_from_db_coin(name, date):
    coin = InputData.query.filter_by(name=name).first()
    if coin is None:
        pass
    calculate_score_for_tweet(coin, date)


def calculate_score_for_tweet(coin, date, token="none"):
    logging.info("Calculating score for ", coin.name)
    tweets = get_tweet_for_input(coin, input_date=date, next_token=token)
    if tweets["meta"]["result_count"] > 0:
        tweets_records = create_scraped_data_records(tweets, coin)
        for tr in tweets_records:
            calculate_sentiment_for_tweet(coin, tr)
        there_is_next_token = "next_token" in tweets["meta"]
        if there_is_next_token:
            token = tweets["meta"]["next_token"]
            calculate_score_for_tweet(coin, date, token)


def create_scraped_data_record(tweets, input_data):
    source = "twitter"
    logging.info("Adding record with ", input_data.id, " from ", source)
    for tweet in tweets["data"]:
        text_data = tweet["text"]
        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))
        if len(text_data) > 260:
            text_data = text_data[0:260]
        database_service.create_and_save_scrape_data(input_data, source, text_data, tweet)






## Get data from csv
def scrape_twitter_from_csv():
    csv_url = "app/jobs/populate.csv"
    logging.info("SCRAPING TWITTER -- ")
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            tweet_count = 1
            input_data = InputData.query.filter_by(name=row["name"]).first()
            if input_data is None:
                continue
            logging.info(input_data.name, " is : ", input_data.id)
            tweets = get_tweet_for_input(input_data=input_data, input_date=row["date"])
            create_scraped_data_record(tweets, input_data)
            there_is_next_token = "next_token" in tweets["meta"]
            if there_is_next_token:
                token = tweets["meta"]["next_token"]
            while there_is_next_token and tweet_count < MAX_TWEETS:
                tweets = get_tweet_for_input(input_data=input_data, input_date=row["date"], next_token=token)
                create_scraped_data_record(tweets, input_data)
                there_is_next_token = "next_token" in tweets["meta"]
                tweet_count += 1
                if there_is_next_token:
                    token = tweets["meta"]["next_token"]


def create_scraped_data_records(tweets, coin):
    source = "twitter"
    logging.info("Adding record with ", coin.id, " from ", source)
    twees_list = []
    for tweet in tweets["data"]:
        text_data = tweet["text"]
        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))
        if len(text_data) > 260:
            text_data = text_data[0:260]
        twees_list.append(ScrapedData(text=text_data,
                                      date=tweet["created_at"],
                                      source=source,
                                      input_data=coin.id))
    return twees_list
