from flask import (Blueprint)
from .scraper.twitter_client import TwitterScraper
bp = Blueprint('/api', __name__, url_prefix='/api')

@bp.route('coins', methods=['GET'])
def index():
    query = "bitcoin or btc"
    tweet_fields = "tweet.fields=text,author_id,created_at"
    json_response = TwitterScraper.search_twitter_in_range(query=query, tweet_fields=tweet_fields)
    return json_response
