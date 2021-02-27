from datetime import datetime

from flask import (Blueprint)
from flask import jsonify

from app.utility.formats import foramt_Y_M_D

bp = Blueprint('/api', __name__, url_prefix='/api')
from app.models import db, InputData, SentimentScore, SentimentMeanScore, TableView
from flask import request


@bp.route('calculate_score', methods=['POST'])
def calculate_score():
    query = {"data": "not_suppeorted_yet"}
    return query


@bp.route('coins', methods=['GET'])
def get_coins():
    page = request.args.get('page', default=1, type=int)
    offset = request.args.get('offset', default=10, type=int)
    list_of_coins = InputData.query.paginate(page, offset, False).items
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
    sentiment_scores = db.session.query(InputData, SentimentScore).join(SentimentScore).filter(
        InputData.name == name).all()
    # sentiment_scores = SentimentScore.query.inn(InputData, SentimentScore.input_data == InputData.id).paginate(page, offset, False).items
    print(sentiment_scores)
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
    sentiment_scores = db.session.query(InputData, SentimentMeanScore).join(SentimentMeanScore).filter(
        InputData.name == name).all()
    # sentiment_scores = SentimentScore.query.inn(InputData, SentimentScore.input_data == InputData.id).paginate(page, offset, False).items
    print(sentiment_scores)
    return jsonify({
        'data': [create_mean_result(input_data, mean_score) for (input_data, mean_score) in sentiment_scores]
    })


@bp.route('table', methods=['GET'])
def get_hype():
    date_today = datetime.now().date()
    hypes = TableView.query.filter(TableView.relative_hype != None, TableView.date==date_today).all()
    return jsonify({
        'data': [hype.serialized for hype in hypes]
    })