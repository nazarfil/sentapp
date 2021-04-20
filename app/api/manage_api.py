import logging
from datetime import datetime
from flask import (Blueprint)
from flask import jsonify

from app.api.api_auth import auth
from app.jobs.calculate_hype_score_job import hype_score_for_coin, hype_score_for_all_coins
from app.jobs.populate_input_data_job import populate_db_api
import app.jobs.populate_price_job as price_job
from app.jobs.twitter_scrape_job import TwitterJob
from app.jobs.update_database import update_score_count, update_string_id, update_description_of_coins, \
    update_description_of_coin, update_order
from app.scraper.coinmarketcap.coinmarketcap_scraper import extract_to_mem
from app.utility.formats import foramt_Y_M_D
from flask import request

manage_bp = Blueprint('/api/manage', __name__, url_prefix='/api/manage')
twitter_job = TwitterJob()



@manage_bp.route("test", methods=["POST"])
@auth.login_required()
def test():
    print("Test")
    return jsonify({'test': "ok"})

## MANAGE API
@manage_bp.route('refresh_coins', methods=["POST"])
@auth.login_required()
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
@auth.login_required()
def scrape_coins():
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    twitter_job.scrape_twitter_from_db(date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('scrape_coins/<name>', methods=["POST"])
@auth.login_required()
def scrape_coins_by_name(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    twitter_job.scrape_twitter_from_db_coin(name, date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('scrape_coins_range', methods=["POST"])
@auth.login_required()
def scrape_coins_range():
    logging.info("Scraping last 15 min")
    twitter_job.scrape_twitter_from_db_range()
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_hype_score/<name>', methods=["POST"])
@auth.login_required()
def calculate_hype_score_by_name(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    hype_score_for_coin(name, date)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_hype_score', methods=["POST"])
@auth.login_required()
def calculate_hype_score():
    hype_score_for_all_coins()
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_financial_history', methods=["POST"])
@auth.login_required()
def calculate_financial_history():
    # start_date = request.args.get('start_date', default=today, type=str)
    # end_date = request.args.get('end_date', default=today, type=str)
    price_job.populate_prices_history()
    return jsonify({'status': "Request was processed"})


@manage_bp.route('calculate_financial_history_all', methods=["POST"])
@auth.login_required()
def calculate_financial_history_all():
    # start_date = request.args.get('start_date', default=today, type=str)
    # end_date = request.args.get('end_date', default=today, type=str)
    start_arg = request.args.get('start_id', default=0, type=int)
    price_job.populate_price_and_market_cap(start_arg)
    return jsonify({'status': "Request was processed"})


@manage_bp.route('update_count', methods=["POST"])
@auth.login_required()
def update_count():
    update_score_count()
    return jsonify({'status': "Request was processed"})


@manage_bp.route('update_id', methods=["POST"])
@auth.login_required()
def update_id():
    update_string_id()
    return jsonify({'status': "Request was processed"})


@manage_bp.route("update_description", methods=["POST"])
@auth.login_required()
def update_description():
    update_description_of_coins()
    return jsonify({'status': "Request was processed"})


@manage_bp.route("update_orders", methods=["POST"])
@auth.login_required()
def update_orders():
    update_order()
    return jsonify({'status': "Request was processed"})


@manage_bp.route("update_description/<coin>", methods=["POST"])
@auth.login_required()
def update_description_by_name(coin):
    name = request.args.get('name', default=coin, type=str)
    update_description_of_coin(coin, name)
    return jsonify({'status': "Request was processed"})
