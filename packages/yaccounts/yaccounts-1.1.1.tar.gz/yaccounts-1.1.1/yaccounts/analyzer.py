import pathlib
import pandas as pd

from .config import CODES_IGNORED, all_handled_codes
from .utils import filter_df_on_operating_units
from .workbook import Workbook


class CsvDataAnalyzer:
    def __init__(self, csv_path, split_notebooks=False) -> None:
        self.csv_path = csv_path
        self.split_notebooks = split_notebooks

        self.df = pd.read_csv(self.csv_path)

        # Convert Operating Unit to string
        self.df["Operating Unit"] = self.df["Operating Unit"].apply(str)

        # Filter out ignored codes (account in CODES_IGNORED)
        self.df = self.df[~self.df["Account"].isin(CODES_IGNORED)]

        self.operating_units = sorted([str(ou) for ou in self.df["Operating Unit"].unique()])
        print(f"Operating Units Found in CSV: {', '.join(self.operating_units)}")

        self.workbooks_initialized = False
        self.workbooks = []

        self.check_unhandled_codes()

    def add_workbook(self, path):
        self.workbooks_initialized = True
        workbook = Workbook(path)
        workbook.analyzer = self
        self.workbooks.append(workbook)
        return workbook

    def _setup_default_workbooks(self):
        if self.split_notebooks:
            # Create a new workbook for each operating unit
            for operating_unit in self.operating_units:
                self.add_workbook(pathlib.Path.cwd() / (operating_unit + ".xlsx")).add_worksheet(
                    operating_unit
                ).add_operating_unit(operating_unit)
        else:
            # Create a single workbook with all operating units
            wb = self.add_workbook(pathlib.Path.cwd() / "all.xlsx")
            for operating_unit in self.operating_units:
                wb.add_worksheet(operating_unit).add_operating_unit(operating_unit)

    def run(self):
        if not self.workbooks_initialized:
            self._setup_default_workbooks()

        for workbook in self.workbooks:
            workbook.run(filter_df_on_operating_units(self.df, workbook.get_operating_units()))

    def check_unhandled_codes(self):
        # Get all account codes that were not handled
        unhandled_codes = sorted(
            self.df[
                (~self.df["Account"].isin(all_handled_codes()))
                & (self.df["JRNL Line Ledger"] == "ACTUALS")
            ]["Account"].unique()
        )

        # TODO: Add to spreadsheet instead of raising exception

        if unhandled_codes:
            raise Exception(
                f"Unhandled account codes: {','.join([str(c) for c in unhandled_codes])}.  See https://finserve.byu.edu/account-revenue-expense"
            )

    def get_all_operating_units(self):
        return [
            ou
            for workbook in self.workbooks
            for worksheet in workbook.worksheets
            for ou in worksheet.operating_units
        ]

    def find(self, operating_unit, year=None):
        operating_uints = [
            ou for ou in self.get_all_operating_units() if ou.operating_unit == str(operating_unit)
        ]
        if year:
            operating_uints = [ou for ou in operating_uints if ou.year == year]
        return operating_uints
