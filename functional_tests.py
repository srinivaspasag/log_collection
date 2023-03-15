import unittest
import requests
from flask import jsonify
import os
from logger import setup_logger

import test_resources.conftest as c
from log_observer import get_last_n_events, fetch_logs_paging

from test_resources import fake_generator

logger = setup_logger()

directory = os.getcwd()


class TestGetLastNEvents(unittest.TestCase):
    def setUp(self):
        # Create a test file with some sample data
        self.base_url = c.HOSTNAME
        # full_path = os.path.join(log_path, log_file)
        self.keyword = None
        self.filepath = None

    def test_get_last_n_events(self):
        n = 100
        self.test_file = fake_generator.generate_data(10000)
        file_path = c.path + "/" + self.test_file

        response = requests.get(
            self.base_url + "/api/v1/log?filename=" + self.test_file + "&n=" + str(n)
        )

        self.assertEqual(response.status_code, 200)
        events = response.json()

        self.filepath = file_path

        # Test that the function returns the last n lines of the file
        lines = fetch_logs_paging(file_path, n, -1, None)
        # result = get_last_n_events(lines, n, self.keyword)
        self.filepath = file_path
        self.assertEqual(lines, events)

    def test_get_last_n_events_invalid_file(self):
        n = 11
        self.test_file = "log_900.txt"
        file_path = c.path + "/" + self.test_file

        response = requests.get(
            self.base_url
            + "/api/v1/log?filename="
            + self.test_file
            + "&n="
            + str(n)
            + "&keyword=event"
        )

        self.assertEqual(response.status_code, 500)

    def test_get_events_keyword_matched(self):
        n = 11
        self.test_file = fake_generator.generate_data(1000)
        file_path = c.path + "/" + self.test_file
        keyword = "message"
        response = requests.get(
            self.base_url
            + "/api/v1/log?filename="
            + self.test_file
            + "&n="
            + str(n)
            + "&keyword="
            + keyword
        )
        self.assertEqual(response.status_code, 200)
        events = response.json()

        # Test that the function returns the last n lines of the file
        log_data = fetch_logs_paging(file_path, n, -1, keyword)

        # result = get_last_n_events(lines, self.count, self.keyword)
        self.assertEqual(log_data, events)

    def tearDown(self):
        # Clean up the test file
        if self.filepath:
            if os.path.isfile(self.filepath):
                os.remove(self.filepath)


if __name__ == "__main__":
    unittest.main()
