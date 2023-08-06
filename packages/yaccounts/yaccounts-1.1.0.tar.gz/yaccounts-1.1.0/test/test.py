""" Unit test of yaccounts package"""

import unittest
import yaml

from yaccounts import CsvDataAnalyzer


class TestBalances(unittest.TestCase):
    def test_balances(self):
        aa = CsvDataAnalyzer("test/data.csv")

        # Load balances yml file
        with open("test/balances.yml") as yaml_file:
            balance_data = yaml.safe_load(yaml_file)

        aa.run()

        for item in balance_data:
            operating_unit = str(item["operating_unit"])
            year = item["year"]
            balance = item["balance"]

            matches = aa.find(operating_unit, year)

            assert int(matches[0].balance) == int(balance)
