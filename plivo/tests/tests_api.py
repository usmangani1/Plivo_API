# !/usr/bin/python
"""
__email__ sgosman_chem@yahoo.com
__author__ Usman Shaik
"""

import unittest
import requests
from src import connections


LOGGER=connections.get_logger()

class TestFlaskApiUsingRequests(unittest.TestCase):

    def test_search_email(self):
        response = requests.get('http://127.0.0.1:9090/contacts/Search/Email?email=sg&start=0')
        LOGGER.info(response.json())
        self.assertEqual(int(response.json()["code"]),200)

    def test_search_name(self):
        response = requests.get('http://127.0.0.1:9090/contacts/Search/Name?name=us&start=0')
        LOGGER.info(response.json())
        self.assertEqual(int(response.json()["code"]), 200)





if __name__ == "__main__":
    unittest.main()