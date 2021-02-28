from datetime import datetime

from flask import (Blueprint)
from flask import jsonify

import app.services.database_service as db_service

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
