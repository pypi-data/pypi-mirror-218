import calendar
from collections import defaultdict
import re
import numpy as np

import pandas as pd

from .config import *


class OperatingUnit:
    def __init__(self, worksheet, operating_unit, name=None, previous_expenditures=0) -> None:
        self.worksheet = worksheet
        self.operating_unit = operating_unit
        self.name = name
        self.previous_expenditures = previous_expenditures

        # Create a new dataframe with months of the year as column headers
        self.df_gen = pd.DataFrame(
            columns=("Type", *[calendar.month_abbr[i] for i in range(1, 13)])
        )

        self.row_colors = {}
        self.hidden_rows = []

        # Default options
        self.set_options()

        self.df = None

    def set_options(self, hide_student_wages=False):
        self.hide_student_wages = hide_student_wages

    def run(self, df):
        self.df = df

        print("Running Operating Unit:", self.operating_unit)

        # Add student wage data
        self.add_row("Student Wages", CODES_STUDENT_WAGES, color=COLOR_STUDENT_WAGES)
        self.create_student_wages()
        self.add_row("Student Benefits", CODES_STUDENT_BENEFITS, color=COLOR_STUDENT_BENEFITS)
        self.add_row("Student Tuition", CODES_STUDENT_TUITION, color=COLOR_STUDENT_TUITION)
        self.add_row("Faculty Spr/Sum", CODES_FACULTY_SPRING_SUMMER, color=COLOR_FACULTY)
        self.add_row("Travel", CODES_TRAVEL, color=COLOR_TRAVEL)
        self.add_row("Supplies/Misc", CODES_SUPPLIES, color=COLOR_SUPPLIES)
        self.add_row("Capital Equipment", CODES_CAPITAL, color=COLOR_CAPITAL)
        self.add_row("Overhead", CODES_OVERHEAD, color=COLOR_OVERHEAD)
        self.row_total_expenses = self.add_row(
            "Total Expeneses", all_expense_codes(), color=COLOR_TOTAL_EXPENSES
        )
        self.add_empty_row()

        self.add_row("Interest", CODES_INTEREST, actuals_coeff=-1)
        self.add_row(
            "Budget (New/Carryover)",
            [],
            budgets_account_codes=CODES_BALANCE_FORWARD,
            budgets_coeff=1,
            actuals_coeff=-1,
        )
        self.row_total_income = self.add_row(
            "Total Income",
            CODES_INTEREST,
            budgets_account_codes=CODES_BALANCE_FORWARD,
            color=COLOR_TOTAL_INCOME,
            budgets_coeff=1,
            actuals_coeff=-1,
        )

        self.add_empty_row()

        # Add a sum column that sums the values in each row, starting with the 2nd column,
        # skipping rows where "Type" is empty

        # Calculate the sum for rows where 'Type' column is not empty
        columns_to_sum = self.df_gen.columns[1:]  # Get all columns starting from the second column
        self.df_gen.loc[self.df_gen["Type"] != "", "Sum"] = self.df_gen.loc[
            self.df_gen["Type"] != "", columns_to_sum
        ].sum(axis=1)

        self.add_balance_row()
        self.add_empty_row()

        self.check_unhandled_codes()

        # self.df_gen["Sum"] = self.df_gen.apply(
        #     lambda row: row["Value"] if row["Type"] else None, axis=1
        # )

        # Add extra row to top of df_gen called "Students"
        # header_row = ["Students"] + [""] * (num_students)
        # df_gen = pd.concat((header_row, df_gen), ignore_index=True)

        # Export df_gen to Excel
        # df_gen.to_excel("out.xlsx", index=False)

        # # Create a new Excel file and add a worksheet.
        # workbook = xlsxwriter.Workbook(f"{operating_unit}.xlsx")
        # worksheet = workbook.add_worksheet()

        # formattedWorksheet = FormattedWorksheet(sheet, workbook, df_gen, hasIndex=True)

        # sheet.insert_row(header_row, 0)
        # sheet.write_row(1, 1, header_row)
        title_name = self.operating_unit
        if self.name:
            title_name = f"{self.name} ({title_name})"
        self.worksheet.write_to_sheet(self.df_gen, title_name, self.hidden_rows, self.row_colors)

        # sheet.set_row(student_total_row, cell_format=blue_fill_format)

    def add_empty_row(self):
        # Add an empty row of None values
        # self.df_gen = pd.concat((self.df_gen, pd.DataFrame([[""] * 13])), ignore_index=True)
        empty_data = {
            "Type": [""],
            **{calendar.month_abbr[month]: [np.nan] for month in range(1, 13)},
        }

        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(empty_data)), ignore_index=True)

        # self.df_gen.insert(
        #     len(self.df_gen), pd.Series([np.nan] * len(self.df_gen.columns)), ignore_index=True
        # )

        # self.df_gen = pd.concat((self.df_gen, pd.DataFrame([[""] * 13])), ignore_index=True)

    def add_row(
        self,
        row_name,
        actuals_account_codes,
        budgets_account_codes=[],
        budgets_coeff=0,
        actuals_coeff=1,
        color=None,
    ):
        """Sum the values in the 'Amount' column for each month in the given account codes.
        If actual=True, then only actual values will be summed.
        Otherwise budgeted (account income) values will be summed."""

        new_row_data = {
            "Type": [row_name],
            **{
                calendar.month_abbr[month]: [
                    budgets_coeff
                    * (
                        self.df.loc[
                            (self.df["Accounting Period"] == month)
                            & (self.df["JRNL Line Ledger"] == "BUDGETS")
                        ][COL_NAME_AMOUNT].sum()
                    )
                    + actuals_coeff
                    * (
                        self.df.loc[
                            (self.df["Accounting Period"] == month)
                            & self.df["Account"].isin(actuals_account_codes)
                            & (self.df["JRNL Line Ledger"] == "ACTUALS")
                        ][COL_NAME_AMOUNT].sum()
                    )
                ]
                for month in range(1, 13)
            },
        }

        # Add this dictionary to the dataframe
        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(new_row_data)), ignore_index=True)

        if color:
            self.row_colors[len(self.df_gen)] = color

        return self.df_gen.tail(1).index[0]

    def add_balance_row(self):
        self.df_gen.loc[len(self.df_gen)] = {
            "Type": "Previous Expenditures",
            calendar.month_abbr[1]: self.previous_expenditures,
        }

        self.df_gen.loc[len(self.df_gen)] = {"Type": "Balance (end of month)"}

        # # Iterate through columns and calcuate the balance, which is the total income minus the total expenses
        for month in range(1, 13):
            self.df_gen.iloc[len(self.df_gen) - 1, month] = (
                self.df_gen.iloc[self.row_total_income][month]
                - self.df_gen.iloc[self.row_total_expenses][month]
                + (
                    self.df_gen.iloc[len(self.df_gen) - 1, month - 1]
                    if month > 1
                    else -self.df_gen.iloc[len(self.df_gen) - 2, month]
                )
            )

        self.row_colors[len(self.df_gen)] = "yellow"

    def create_student_wages(self):
        # Filter to only student wages ('Account' column in STUDENT_WAGES)
        df_students = self.df[
            (self.df["Account"].isin(CODES_STUDENT_WAGES))
            & (self.df["JRNL Line Ledger"] == "ACTUALS")
        ]

        # Get unique list of value in 'JRNL Line Descr' column
        students_raw = df_students["JRNL Line Descr"].unique()
        students = defaultdict(list)
        for student in students_raw:
            match = re.search("([A-Za-z]+)[, ]+([A-Za-z]+)", student)
            if not match:
                raise Exception(f"Could not parse student name: {student}")
            student_key = f"  {match.group(2).title()} {match.group(1).title()}"
            students[student_key].append(student)

        # Create a new dictionary with the student wages by month
        student_data = {
            "Type": [s for s in sorted(students.keys())],
            **{
                calendar.month_abbr[month]: [
                    df_students.loc[
                        (df_students["Accounting Period"] == month)
                        & (df_students["JRNL Line Descr"].isin(students[student]))
                    ]["JRNL Monetary Amount -no scrn aggregation"].sum()
                    for student in sorted(students.keys())
                ]
                for month in range(1, 13)
            },
        }
        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(student_data)), ignore_index=True)

        # Add new row index to hidden rows
        if self.hide_student_wages:
            self.hidden_rows.extend(
                range(len(self.df_gen) - len(student_data["Type"]) + 1, len(self.df_gen) + 1)
            )

    def check_unhandled_codes(self):
        # Get all account codes that were not handled
        unhandled_codes = self.df[
            (~self.df["Account"].isin(all_handled_codes()))
            & (self.df["JRNL Line Ledger"] == "ACTUALS")
        ]["Account"].unique()

        # TODO: Add to spreadsheet instead of raising exception

        if unhandled_codes.size > 0:
            raise Exception(
                f"Unhandled account codes: {','.join([str(c) for c in unhandled_codes])}.  See https://finserve.byu.edu/account-revenue-expense"
            )
