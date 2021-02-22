from app.jobs.search_tweets_for_input import *
import unittest

class TestTweeterApiQuery(unittest.TestCase):
    def test_date_formatter(self):
        input_date = '2021-02-19'
        result_start, result_end = get_datetime_from_string(input_date)
        print(result_start, result_end)
        self.assertEqual("2021-02-19T00:00:01Z", result_start)
        self.assertEqual("2021-02-19T23:59:59Z", result_end)

    def test_day_not_in_range(self):
        date_in =  "2020-12-20"
        in_range = check_if_date_in_range(date_in, 7)
        self.assertFalse(in_range)

    def test_day_in_range(self):
        date_today = datetime.today()
        input_format = "%Y-%m-%d"
        in_range = check_if_date_in_range(date_today.strftime(input_format), 7)
        self.assertTrue(in_range)