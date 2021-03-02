from redis import Redis
import rq


def call_twitter(i):
    print("Calling twitter for", i)
    return [i + 2, i + 3]


def refresh_data():
    for i in range(10):
        tweets = call_twitter(i)
        print("GOT tweets", tweets)


def calculate_score(tweet):
    return "GOOD"


def update_scores():
    tweets = [1, 2]
    for tweet in tweets:
        score = calculate_score(tweet)
        print("SCORE : ", score)
