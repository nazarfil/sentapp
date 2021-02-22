import csv
from .search_tweets_for_input import get_tweet_for_input
from app.models import ScrapedData, db, InputData
import re

def scrape_twitter_from_csv():
    csv_url = "app/jobs/populate.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            input_data = InputData.query.filter_by(name=row["name"]).first()
            if input_data is None:
                continue
            tweets = get_tweet_for_input(input_data=input_data, input_date=row["date"])
            create_scraped_data_record(tweets, input_data)
            there_is_next_token = "next_token" in tweets["meta"]
            if there_is_next_token:
                token = tweets["meta"]["next_token"]
            while there_is_next_token:
                tweets = get_tweet_for_input(input_data=input_data, input_date=row["date"], next_token=token)
                create_scraped_data_record(tweets, input_data)
                there_is_next_token = "next_token" in tweets["meta"]
                if there_is_next_token:
                    token = tweets["meta"]["next_token"]


def create_scraped_data_record(tweets, input_data):
    source = "twitter"
    for tweet in tweets["data"]:
        text_data = tweet["text"]
        text_data = " ".join(filter(lambda x: x[0] != '@', text_data.split()))
        if len(text_data)>260:
            text_data = text_data[0:260]
        scraped_data = ScrapedData(text=text_data,
                                   date=tweet["created_at"],
                                   source=source,
                                   input_data=input_data.id)

        db.session.add(scraped_data)
        db.session.commit()