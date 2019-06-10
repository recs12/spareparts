#!python3
# -*- coding: utf-8 -*-
"""Spreadsheet Column Printer

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This tool accepts comma separated value files (.csv) as well as excel
(.xls, .xlsx) files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

from glob import glob
import os
import sys
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')
import pandas as pd

def proceed_yes_or_no():
    print(f"Run: {__file__}")
    answer = input("Proceed ([y]/n) ?:  ")
    if answer in ['yes', 'y', 'YES', 'Y']:
        pass
    else:
        sys.exit("Process has stopped.")

def spl_and_requisition_listmaker(location):
    """spl_and_requisition_listmaker(location) -> (spl, requisistion)"""
    list_files = [n.name for n in os.scandir(location)]
    files = pd.Series(list_files)
    not_req = files[~files.str.contains(r'.*REQ.*\.(xlsm|xlsx)', regex=True)]
    req = files[files.str.contains(r'.*REQ.*\.(xlsm|xlsx)', regex=True)]
    return (not_req, req)

def parse_requisition(file_name):
    """Parse one column: Item number."""
    dataframe = pd.read_excel(file_name, header=10, index_col=False, index=False)
    data = dataframe['No. Item'].dropna()
    data = data[1:]
    data.str.strip()
    return data

def requisition_database_builder(requisitions_list):
    """"""
    req = pd.concat([parse_requisition(i) for i in requisitions_list])
    list_req = req.unique().tolist()
    dataframe = pd.DataFrame({'item_number':list_req, 'possibility':'R'})
    return dataframe

def requisition_database_filter(data, data_req):
    data_item_number_listed = data.item_number.tolist()
    new_data_req = data_req.loc[~data_req.item_number.isin(data_item_number_listed), :]
    return new_data_req

def concat(listing):
    """merge the data of all excel file the same dataframe with pandas"""
    return pd.concat([extract_levels(file) for file in listing], ignore_index=True)

def rows_empty(dataframe):
    """Remove empty rows in column: item number"""
    return dataframe[~dataframe.item_number.isin(['nan'])]

def assign_levels(dataframe):
    #create a new column with the level for each row
    equivalences = {
        'Level 3: Complete Parts Inventory': 3,
        'Level 2: Useful Parts': 2,
        'Level 1: Critical Parts': 1,
        '1': 1,
        '2': 2,
        '3': 3,
    }
    dataframe['level'] = dataframe.level_of_significance.map(equivalences, na_action=None)
    return dataframe

def extract_levels(file):
    """
    Extraction of the data from the excel SPL file
    item number  | level of significance(text string)
    """
    dataframe = pd.read_excel(file, sheet_name=1, header=1, usecols="A,F", dtype={0:str, 1:str})
    dataframe.columns = dataframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dataframe = dataframe.dropna(how='all')
    return dataframe

def two_columns_ordered(dataframe):
    levels = dataframe[['item_number', 'level']]
    levels_ordered = levels.sort_values(by='item_number')
    levels_ordered['Level 1: Critical Parts'] = levels_ordered.level.map({1:1, 2:0, 3:0})
    levels_ordered['Level 2: Useful Parts'] = levels_ordered.level.map({1:0, 2:1, 3:0})
    levels_ordered['Level 3: Complete Parts Inventory'] = levels_ordered.level.map({1:0, 2:0, 3:1})
    levels_ordered.set_index('item_number')
    dataframe = levels_ordered.groupby(['item_number'], as_index=False)[
        'Level 1: Critical Parts',
        'Level 2: Useful Parts',
        'Level 3: Complete Parts Inventory'
    ].sum()
    return dataframe

def create_three_bool_columns(dataframe):
    dataframe['L1'] = dataframe['Level 1: Critical Parts'].astype(bool).map({True:1, False:0})
    dataframe['L2'] = dataframe['Level 2: Useful Parts'].astype(bool).map({True:1, False:0})
    dataframe['L3'] = dataframe['Level 3: Complete Parts Inventory'].astype(bool).map({True:1, False:0})
    return dataframe

def create_column_possibility(dataframe):
    """create columns: possibility"""
    dataframe.loc[(dataframe.L1 == 1), 'possibility'] = "1"
    dataframe.loc[(dataframe.L2 == 1), 'possibility'] = "2"
    dataframe.loc[(dataframe.L3 == 1), 'possibility'] = "3"
    dataframe.loc[(dataframe.L1 == 1) & (dataframe.L2 == 1), 'possibility'] = "1|2"
    dataframe.loc[(dataframe.L2 == 1) & (dataframe.L3 == 1), 'possibility'] = "2|3"
    dataframe.loc[(dataframe.L1 == 1) & (dataframe.L2 == 1) & (dataframe.L3 == 1), 'possibility'] = "1|2|3"
    return dataframe

def create_csv(dataframe, name='db.csv'):
    dataframe.to_csv(name, index=False)
    print(f'Task compeleted: -> {name} created')


def fill_possibility_with_question_mark(dataframe):
    dataframe['possibility'].fillna(0, inplace=True)
    return dataframe

def info_to_print(spl, requisitions):
    if (spl.empty and requisitions.empty):
        print("no spl or requisitions in the folder")
    else:
        qty_spl, qty_requisition = len(spl), len(requisitions)
        print(f"number of excel files : {qty_spl + qty_requisition} (spl:{qty_spl}, requisition:{qty_requisition})")

def main():
    proceed_yes_or_no()
    spls, requisitions = spl_and_requisition_listmaker('.')
    info_to_print(spls, requisitions)
    data = concat(spls)
    data = rows_empty(data)
    data = assign_levels(data)
    data = two_columns_ordered(data)
    data = create_three_bool_columns(data)
    data = create_column_possibility(data)
    data = fill_possibility_with_question_mark(data)
    data_req = requisition_database_builder(requisitions)
    data_req = requisition_database_filter(data, data_req)
    data = pd.concat([data, data_req], sort=False)
    create_csv(data)

if __name__ == "__main__":
    main()



#TODO: When there is no REQ the program crashes bug to fix.