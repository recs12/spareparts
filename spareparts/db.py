#!python3
# -*- coding: utf-8 -*-

from glob import glob
import os
import sys
import warnings

warnings.filterwarnings("ignore", "This pattern has match groups")
import pandas as pd
import click


class Levels:
    """
    Determinate the level of parts.
    It provides the .csv file being used with spareparts macro. 
    """

    def __init__(self):
        self.loc = os.getcwd()
        self.spls = [
            spreadsheet.name
            for spreadsheet in os.scandir(self.loc)
            if spreadsheet.name.endswith(".xlsm")
        ]
        self.levels = pd.concat(
            [Levels.extract_levels(file) for file in self.spls], ignore_index=True
        )
        self.brut = None
        self.modules = None

    @staticmethod
    def proceed_validation():
        print(f"Run: {__file__}")
        answer = input("Proceed ([y]/n) ?:  ")
        if answer.lower() in ["yes", "y"]:
            pass
        else:
            print("Process cancelled.")
            sys.exit()

    def info(self):
        print(self.spls)

    def del_empty_rows(self):
        """Remove empty rows in column: item number"""
        self.levels = self.levels[~self.levels.item_number.isin(["nan"])]

    def assign_levels(self):
        """create a new column with the level for each row"""
        equivalences = {
            "Level 3: Complete Parts Inventory": 3,
            "Level 2: Useful Parts": 2,
            "Level 1: Critical Parts": 1,
            "1": 1,
            "2": 2,
            "3": 3,
        }
        self.levels["level"] = self.levels.level_of_significance.map(
            equivalences, na_action=None
        )

    def generate_brut(self):
        """
        Brut dataframe is a support for creating <db.csv> 
        brut add to extra dimensional categories : equipment & module
        """
        self.brut = self.levels[["item_number", "module", "level"]]
        # #01 >>> 01
        pat = r"#(?P<numero>\d\d).*"
        repl = lambda m: m.group("numero")
        self.brut.loc[:,"module"] = self.brut["module"].str.replace(pat, repl, regex=True)
        # 01-AAA >>> 01
        pat = r"(?P<numero>\d\d).*"
        repl = lambda m: m.group("numero")
        self.brut.loc[:,"module"] = self.brut.loc[:,"module"].str.replace(pat, repl, regex=True)
        self.brut.loc[:,"module"] = self.brut.loc[:,"module"].str.replace(
            "^1$", "01", regex=True
        )  # 1 >>> 01
        self.brut.loc[:,"module"] = self.brut["module"][
            self.brut.loc[:,"module"] != "0"
        ]  # remove 0
        self.brut.loc[:,"module"] = self.brut["module"][
            self.brut.loc[:,"module"].str.len() == 2
        ]  # only the two caracter long module name kept
        self.brut = self.brut.dropna(
            subset=["item_number", "module"]
        )  # drop empty rows
        self.brut = self.brut.drop_duplicates()
        self.brut = self.brut.sort_values(
            by=["item_number", "module", "level"], ascending=True
        )
        self.brut = self.brut.drop_duplicates(
            subset=["item_number", "module"], keep="first"
        )

    @staticmethod
    def extract_levels(file):
        """
        Extraction of the data from the excel SPL file
        item number  || Equipment || Module || level of significance(text string)
        """
        dataframe = pd.read_excel(
            file,
            sheet_name=1,
            header=1,
            usecols="A,D,E,F",
            dtype={0: str, 1: str, 2: str, 3: str},
        )
        dataframe.columns = (
            dataframe.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        dataframe = dataframe.dropna(how="all")
        return dataframe

    def two_columns_ordered(self):
        self.levels = self.levels.sort_values(by="item_number")
        self.levels["Level 1: Critical Parts"] = self.levels.level.map(
            {1: 1, 2: 0, 3: 0}
        )
        self.levels["Level 2: Useful Parts"] = self.levels.level.map({1: 0, 2: 1, 3: 0})
        self.levels["Level 3: Complete Parts Inventory"] = self.levels.level.map(
            {1: 0, 2: 0, 3: 1}
        )
        self.levels.set_index("item_number")
        self.levels = self.levels.groupby(["item_number"], as_index=False)[
            "Level 1: Critical Parts",
            "Level 2: Useful Parts",
            "Level 3: Complete Parts Inventory",
            "module",
        ].sum()
        # add the missing columns at the end of the method

    def insert_bool_columns(self):
        self.levels["L1"] = (
            self.levels["Level 1: Critical Parts"].astype(bool).map({True: 1, False: 0})
        )
        self.levels["L2"] = (
            self.levels["Level 2: Useful Parts"].astype(bool).map({True: 1, False: 0})
        )
        self.levels["L3"] = (
            self.levels["Level 3: Complete Parts Inventory"]
            .astype(bool)
            .map({True: 1, False: 0})
        )

    def insert_column_possibility(self):
        """create columns: possibility"""
        self.levels.loc[(self.levels.L1 == 1), "possibility"] = "1"
        self.levels.loc[(self.levels.L2 == 1), "possibility"] = "2"
        self.levels.loc[(self.levels.L3 == 1), "possibility"] = "3"
        self.levels.loc[
            (self.levels.L1 == 1) & (self.levels.L2 == 1), "possibility"
        ] = "1|2"
        self.levels.loc[
            (self.levels.L2 == 1) & (self.levels.L3 == 1), "possibility"
        ] = "2|3"
        self.levels.loc[
            (self.levels.L1 == 1) & (self.levels.L2 == 1) & (self.levels.L3 == 1),
            "possibility",
        ] = "1|2|3"

    def fill_zero(self):
        self.levels["possibility"].fillna(0, inplace=True)

    def create_csv(self, name="levels.csv"):
        self.levels.to_csv(name, index=False)
        print(f"\nTask compeleted: -> {name} created")

    def create_col_modules(self):
        s = pd.Series(self.levels["module"], index=None)
        # #01 >>> 01
        pat = r"#(?P<numero>\d\d).*"
        repl = lambda m: m.group("numero")
        s = s.str.replace(pat, repl, regex=True)
        # 01-AAA >>> 01
        pat = r"(?P<numero>\d\d).*"
        repl = lambda m: m.group("numero")
        s = s.str.replace(pat, repl, regex=True)
        s = s.str.replace("^1$", "01", regex=True)  # 1 >>> 01
        s = s[s != "0"]  # remove 0
        s = s[s.str.len() == 2]  # only the two characters long module name are kept.
        s = s.unique()
        self.modules = s

    def insert_col_modules(self):
        for col in self.modules.tolist():
            self.levels[col] = 0

    def set_values_modules(self):
        ambiguous = self.levels[
            ~(
                (self.levels.possibility == "1")
                | (self.levels.possibility == "2")
                | (self.levels.possibility == "3")
            )
        ]
        ambiguous_items = ambiguous["item_number"].tolist()
        modules_levels = self.modules.tolist()
        modules_levels  # [16, 17, ... ,99]
        data_available = self.brut.item_number.tolist()
        for item in ambiguous_items:
            if item in data_available:
                value_level = self.brut.set_index(["item_number", "module"])
                value_level = value_level.xs(
                    item, level="item_number"
                )  # columns: module, level
                for mod in modules_levels:
                    if mod in value_level.index:
                        level = value_level.loc[mod, "level"]
                        self.levels.loc[self.levels.item_number == item, mod] = level


if __name__ == "__main__":
    db = Levels()
    db.proceed_validation()
    db.info()
    db.del_empty_rows()
    db.assign_levels()
    db.generate_brut()
    db.create_col_modules()
    db.two_columns_ordered()
    db.insert_bool_columns()
    db.insert_column_possibility()
    db.fill_zero()
    db.insert_col_modules()
    db.set_values_modules()
    db.create_csv()

# TODO: Change name to "levels+ date" of genereted file add date on file name
# TODO: clean up print out on display when running the macro
