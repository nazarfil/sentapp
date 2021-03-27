import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (Blueprint)
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from app.jobs.calculate_hype_score_job import hype_score_for_coin, hype_score_for_all_coins
from app.jobs.populate_input_data_job import populate_db_api
import app.jobs.populate_price_job as price_job
from app.jobs.twitter_scrape_job import scrape_twitter_from_db, scrape_twitter_from_db_coin
from app.jobs.update_count import update_score_count
from app.scraper.coinmarketcap.coinmarketcap_scraper import extract_to_mem
from app.utility.formats import foramt_Y_M_D
from flask import request

manage_bp = Blueprint('/api/manage', __name__, url_prefix='/api/manage')
# Basic auth
auth = HTTPBasicAuth()
users = {
    "nazar": generate_password_hash("hello")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


## MANAGE API
@manage_bp.route('refresh_coins', methods=["POST"])
def refresh_coins():
    # Extracting coins from CoinMarketCap
    try:
        logging.info("Refreshing coins data")
        coins = extract_to_mem()
        for coin in coins:
            populate_db_api(coin, 'api')
    except:
        logging.error("Unable to refresh coins data")
    return jsonify({'status': "Request was processed"})


@manage_bp.route('scrape_coins', methods=["POST"])
def scrape_coins():
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    scrape_twitter_from_db(date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('scrape_coins/<name>', methods=["POST"])
def scrape_coins_by_name(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    scrape_twitter_from_db_coin(name, date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_hype_score/<name>', methods=["POST"])
def calculate_hype_score_by_name(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    hype_score_for_coin(name, date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_hype_score', methods=["POST"])
def calculate_hype_score():
    hype_score_for_all_coins()
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_financial_history', methods=["POST"])
def calculate_financial_history():
    #start_date = request.args.get('start_date', default=today, type=str)
    #end_date = request.args.get('end_date', default=today, type=str)
    price_job.populate_prices_history()
    return jsonify({'status': "Request was processed"})



@manage_bp.route('calculate_financial_history_all', methods=["POST"])
def calculate_financial_history_all():
    #start_date = request.args.get('start_date', default=today, type=str)
    #end_date = request.args.get('end_date', default=today, type=str)
    start_arg = request.args.get('start_id', default=0, type=int)
    price_job.populate_price_and_market_cap(start_arg)
    return jsonify({'status': "Request was processed"})




@manage_bp.route('update_count', methods=["POST"])
def update_count():
    update_score_count()
    return jsonify({'status': "Request was processed"})

