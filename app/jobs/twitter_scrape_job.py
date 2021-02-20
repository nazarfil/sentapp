import csv
from .populate_tweets_for_input import get_tweet_for_input


def scrape_twitter_from_csv():
    csv_url = "app/jobs/populate.csv"
    with open(csv_url, newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            print(get_tweet_for_input(row["name"], row["date"]))
