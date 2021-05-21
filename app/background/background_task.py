from os import environ

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import requests

from app import log, Config

logger = log.def_logger

uri = "http://localhost:5000/api/manage"
refresh = "/refresh_coins"
scrape_coins = "/scrape_coins"
calculate_hype = "/calculate_hype_score"
calculate_financial_history = "/calculate_financial_history_all"
periodic_update = "/scrape_coins_range"
update_reddit = "/update_redditors"

config = Config()
USERNAME = config.API_OAUTH_USERNAME
PASSWORD = config.API_OAUTH_PASSWORD


def scrape_marketcap():
    logger.info("Rescraping coinmarketcap")
    requests.post(url=uri + refresh)


def update_reddit_call():
    logger.info("Rescraping reddit")
    requests.post(url=uri + update_reddit)

def scrape_twitter_and_add_scores():
    logger.info("Rescraping twitter and calculating scores")
    requests.post(url=uri + scrape_coins)


def recalculate_hype():
    logger.info("Calculating hypes  ")
    requests.post(url=uri + calculate_hype)


def recalculate_financial_history():
    logger.info("Calculating financial data  ")
    requests.post(url=uri + calculate_financial_history)


def periodical_refresh():
    logger.info("Periodic refresh")
    requests.post(url=uri + periodic_update, auth=(USERNAME, PASSWORD))


def run_scheduled_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=periodical_refresh, trigger="cron", hour='*', minute='1,33')
    scheduler.add_job(func=update_reddit_call, trigger="cron", day='*', hour = 12, minute = 25)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
