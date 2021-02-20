from app.models import db, InputData, ScrapedData
from app.scraper.twitter_client import TwitterScraper
from datetime import datetime


def get_tweet_for_input(input_name, input_date):
    input_data = InputData.query.filter_by(name=input_name).first()
    query = "{} or {}".format(input_data.name, input_data.ticker)
    tweet_fields = "tweet.fields=text,author_id,created_at"
    TwitterScraper.search_twitter(query=query, tweet_fields=tweet_fields, since=input_date, until=input_date)


def get_datetime_from_string(date):
    start = "00:00:01+0000"
    end = "23:59:59+0000"
    input_format = "%Y-%m-%dT%H:%M:%S%z"
    date_obj_start = datetime.strptime("{}T{}".format(date, start), input_format)
    date_obj_end = datetime.strptime("{}T{}".format(date, end), input_format)
    return date_obj_start.strftime(input_format), date_obj_end.strftime(input_format)