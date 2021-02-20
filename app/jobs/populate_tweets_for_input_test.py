from populate_tweets_for_input import *
import unittest

class TestTweeterApiQuery(unittest.TestCase):
    def test_one(self):
        input_date = '2021-02-19'
        result_start, result_end = get_datetime_from_string(input_date)
        print(result_start, result_end)
        self.assertEqual("2021-02-19T00:00:01Z", result_start)
        self.assertEqual("2021-02-19T23:59:59Z", result_end)
