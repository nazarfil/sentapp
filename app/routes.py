from datetime import datetime

from flask import (Blueprint)
from flask import jsonify

import app.services.database_service as db_service
from app import populate_db_from_csv, hype_score_from_csv
from app.jobs.populate_input_data import populate_db_api
from app.jobs.twitter_scrape_job import scrape_twitter_from_db, scrape_twitter_from_db_coin
from app.utility.coinmarketcap_scraper import extract_to_mem
from app.utility.formats import foramt_Y_M_D

bp = Blueprint('/api', __name__, url_prefix='/api')
from flask import request


@bp.route('calculate_score', methods=['POST'])
def calculate_score():
    query = {"data": "not_suppeorted_yet"}
    return query


@bp.route('coins', methods=['GET'])
def get_coins():
    page = request.args.get('page', default=1, type=int)
    offset = request.args.get('offset', default=10, type=int)
    list_of_coins = db_service.query_input_data_paged(page, offset)
    return jsonify({
        'data': [result.serialized for result in list_of_coins]
    })


def create_result(input_data, score):
    return {
        "name": input_data.name,
        "score": score.sentiment,
        "date": score.date
    }


@bp.route('scores/<name>', methods=['GET'])
def get_scores(name):
    sentiment_scores = db_service.query_join_input_and_sentiment_by_name(name)
    return jsonify({
        'data': [create_result(input_data, score) for (input_data, score) in sentiment_scores]
    })


def create_mean_result(input_data, mean_score):
    return {
        "name": input_data.name,
        "score": mean_score.sentiment,
        "date": mean_score.date
    }


@bp.route('mean_scores/<name>', methods=['GET'])
def get_mean_scores(name):
    sentiment_scores = db_service.query_sentiment_mean_score_for_coin(name)
    return jsonify(
        {'data': [create_mean_result(input_data, mean_score) for (input_data, mean_score) in sentiment_scores]})


@bp.route('table', methods=['GET'])
def get_hype():
    hypes = db_service.query_table_view()
    return jsonify({'data': [hype.serialized for hype in hypes]})


@bp.route('refresh_coins', methods=["GET"])
def refresh_coins():
    # Extracting coins from CoinMarketCap
    try:
        print("Refreshing coins data")
        coins = extract_to_mem()
        for coin in coins:
            populate_db_api(coin)
    except:
        print("Unable to refresh coins data")
    return jsonify({'status': "Request was processed"})


@bp.route('scrape_coins', methods=["POST"])
def scrape_all_coins():
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    scrape_twitter_from_db(date)


@bp.route('scrape_coins/<name>', methods=["POST"])
def scrape_coin(name):
    today = datetime.today().date().strftime(foramt_Y_M_D)
    date = request.args.get('date', default=today, type=str)
    scrape_twitter_from_db_coin(name, date)


@bp.route('calculate_mean_score')
def calculate_mean_score():
    hype_score_from_csv()
