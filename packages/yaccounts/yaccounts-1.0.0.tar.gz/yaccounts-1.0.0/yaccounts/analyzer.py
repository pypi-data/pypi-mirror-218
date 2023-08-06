import pathlib
import pandas as pd

from .utils import filter_df_on_operating_units
from .workbook import Workbook
from .worksheet import Worksheet


class CsvDataAnalyzer:
    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path

        self.df = pd.read_csv(self.csv_path)
        self.df["Operating Unit"] = self.df["Operating Unit"].apply(str)

        self.operating_units = [str(ou) for ou in self.df["Operating Unit"].unique()]
        print(f"Operating Units Found in CSV: {', '.join(self.operating_units)}")

        self.workbooks_initialized = False
        self.workbooks = []

    def set_operating_unit_groups(self):
        # Allow custom groupings of operating units
        raise NotImplementedError

    def add_workbook(self, path):
        self.workbooks_initialized = True
        workbook = Workbook(path)
        self.workbooks.append(workbook)
        return workbook

    def _one_operating_unit_per_workbook(self):
        # Create a new workbook for each operating unit
        for operating_unit in self.operating_units:
            self.workbooks.append(
                Workbook(
                    pathlib.Path.cwd() / (operating_unit + ".xlsx"), [Worksheet(operating_unit)]
                )
            )

    def run(self):
        if not self.workbooks_initialized:
            self._one_operating_unit_per_workbook()

        for workbook in self.workbooks:
            workbook.run(filter_df_on_operating_units(self.df, workbook.get_operating_units()))
