from flask import (Blueprint)
from flask import jsonify
bp = Blueprint('/api', __name__, url_prefix='/api')
from app.models import db, InputData
from flask import request


@bp.route('calculate_score', methods=['POST'])
def calculate_score():
    query = {"data": "not_suppeorted_yet"}
    return query


@bp.route('coins', methods=['GET'])
def get_coins():
    page = int(request.args.get("page"))
    offset = int(request.args.get("offset"))
    list_of_coins = InputData.query.paginate(page, offset, False).items
    return jsonify({
        'data': [result.serialized for result in list_of_coins]
    })


@bp.route('scores', methods=['GET'])
def get_scores():
    query = "bitcoin or btc"
    return query


@bp.route('mean_scores', methods=['GET'])
def get_mean_scores():
    query = "bitcoin or btc"
    return query
