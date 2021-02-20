from app.models import db, InputData, ScrapedData
from app.scraper.twitter_client import TwitterScraper
from datetime import datetime


def get_tweet_for_input(input_name, input_date):
    input_data = InputData.query.filter_by(name=input_name).first()
    print("INPUT DATA IS ",input_data)
    query = "{} or {}".format(input_data.name, input_data.ticker)
    tweet_fields = "tweet.fields=text,author_id,created_at"
    start, end = get_datetime_from_string(input_date)
    return TwitterScraper.search_twitter_in_range(query=query, tweet_fields=tweet_fields, since=start, until=end)


def get_datetime_from_string(date):
    start = "00:00:01Z"
    end = "23:59:59Z"
    input_format = "%Y-%m-%dT%H:%M:%S%z"
    out_f = "%Y-%m-%dT%H:%M:%S%Z"
    date_obj_start = datetime.strptime("{}T{}".format(date, start), input_format)
    date_obj_end = datetime.strptime("{}T{}".format(date, end), input_format)
    return date_obj_start.strftime(out_f).replace('UTC', 'Z'), date_obj_end.strftime(out_f).replace('UTC', 'Z')