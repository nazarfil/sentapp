# Standard library imports...
from unittest.mock import Mock, patch
from app.scraper.twitter.twitter_scraper import search_twitter
from nose.tools import assert_is_not_none,assert_dict_equal


@patch('app.scraper.twitter_service.requests.request')
def test_request_response(mock_get):
    # Configure the mock to return a response with an OK status code.
    mocked_response = {
    "data": [
        {
            "id": "1362567487766855680",
            "text": "Thank you @NYC_DOT - #34AveOpenStreets will resume tomorrow morning. https://t.co/C4H45AK3YU",
            "lang": "en",
            "geo": {
                "place_id": "12e7bb1950d71000"
            },
            "created_at": "2021-02-19T00:59:39.000Z"
        }
        ],
        "meta": {
            "newest_id": "1362567487766855680",
            "oldest_id": "1362567456439623680",
            "result_count": 10,
            "next_token": "b26v89c19zqg8o3fosns2zcnirl47askrr82f554dw5fh"
        }
    }
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = mocked_response
    query = "twitter"
    query_response = search_twitter(query)
    assert_is_not_none(query_response)
    assert_dict_equal(query_response, mocked_response)


