from datetime import datetime, timedelta

from app.scraper.twitter.twitter_scraper import search_twitter
from app.utility.formats import *


def get_tweet_for_input(input_data, input_date, next_token='none'):
    query = build_tweet_query(input_data)
    start, end = get_datetime_from_string(input_date)
    if next_token == 'none':
        return search_twitter(query=query, start_time=start, end_time=end)
    else:
        return search_twitter(query=query, start_time=start, end_time=end, next_token=next_token)


def get_tweets_for_range(input_data, start_date, end_date, next_token):
    query = build_tweet_query(input_data)
    if next_token == 'none':
        return search_twitter(query=query, start_time=start_date, end_time=end_date)
    else:
        return search_twitter(query=query, start_time=start_date, end_time=end_date, next_token=next_token)


def build_tweet_query(input_data):
    common_names = ["Avalanche", "Dash", "Maker", "Compound", "Waves", "Dent", "Neo", "Harmony"]
    ticker = input_data.ticker
    name = input_data.name
    url_encoded_hashtag = "%23"
    if name in common_names:
        name = url_encoded_hashtag + name

    return "({} OR {} OR {}{} OR {}{}) and -is:retweet".format(name, name.lower(), url_encoded_hashtag, ticker , url_encoded_hashtag, ticker.lower())


def get_datetime_from_string(date):
    start = "00:00:01Z"
    end = "23:59:59Z"
    today = datetime.today().date().strftime(foramt_Y_M_D)
    if today == date:
        end = (datetime.now() - timedelta(minutes=61)).strftime(format_H_M_S) + "Z"

    input_format = format_T_H_M_S_Z
    out_f = format_T_H_M_S_ZZ
    date_obj_start = datetime.strptime("{}T{}".format(date, start), input_format)
    date_obj_end = datetime.strptime("{}T{}".format(date, end), input_format)
    return date_obj_start.strftime(out_f).replace('UTC', 'Z'), date_obj_end.strftime(out_f).replace('UTC', 'Z')


def check_if_date_in_range(date, days_range):
    date_obj = datetime.strptime(date, foramt_Y_M_D)
    today = datetime.today()
    diff = today - date_obj
    return diff.days < days_range
