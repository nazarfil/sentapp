from populate_tweets_for_input import *
import unittest

class TestTweeterApiQuery(unittest.TestCase):
    def test_one(self):
        input_date = '2021-02-19'
        result_start, result_end = get_datetime_from_string(input_date)
        self.assertEqual("{}T{}".format(input_date, "00:00:01+0000"), result_start)
        self.assertEqual("{}T{}".format(input_date, "23:59:59+0000"), result_end)
