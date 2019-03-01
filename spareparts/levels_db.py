#!python3
# -*- coding: utf-8 -*-
"""
levels.py : create a database associating -->  jdeitem & level 
using a sample of SPL lists supplied in the same folder 
"""

import os
import sys
from glob import glob
import numpy as np
import pandas as pd
import xlwings as xw
import pprint
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups') #annoying warning 

def proceed_yes_or_no():
    "ask user to resume the program"
    print(f"Run: {__file__}")
    answer = input("Proceed ([y]/n) ?:  ")
    if answer in ['yes','y','YES','Y']:
        pass
    else:
        sys.exit("Process has stopped.")
        
def spl_and_requisition_listmaker(location):
    """spl_and_requisition_listmaker(location) -> (spl,requisistion) """
    list_files = [n.name for n in os.scandir(location)]
    s = pd.Series(list_files)
    # s1 = s[~s.str.contains(r'REQ')]
    # s2 = s[s.str.contains(r'REQ')]
    s1 = s[~s.str.contains(r'.*REQ.*\.(xlsm|xlsx)', regex=True)]
    s2 = s[s.str.contains(r'.*REQ.*\.(xlsm|xlsx)', regex=True)]
    return (s1,s2)

def parse_requisition(file_name):
    df = pd.read_excel(file_name, header=10, index_col=False, index=False)
    db = df['No. Item'].dropna()
    db = db[1:]
    db.str.strip()
    return db

def requisition_database_builder(requisitions_list):
    req = pd.concat([parse_requisition(i) for i in requisitions_list])
    list_req = req.unique().tolist()
    df = pd.DataFrame({'item_number':list_req, 'possibility':'R'})
    return df

def requisition_database_filter(db , db_req): 
    db_item_number_listed = db.item_number.tolist()
    new_db_req = db_req.loc[~db_req.item_number.isin(db_item_number_listed),:]
    return new_db_req
    
def concat(listing):
    """merge the data of all excel file the same dataframe with pandas"""
    return pd.concat([extract_levels(file) for file in listing], ignore_index=True)

def rows_empty(df):
    """filter the empty rows"""
    return df[~df.item_number.isin(['nan'])]

def assign_levels(df):
    #create a new column with the level for each row
    dk = {
    'Level 3: Complete Parts Inventory': 3,
    'Level 2: Useful Parts': 2,
    'Level 1: Critical Parts': 1,
    '1': 1,
    '2': 2,
    '3': 3,
    }
    df['level'] = df.level_of_significance.map(dk, na_action=None)
    return df

def extract_levels(file):
    """extraction of the data from the excel SPL file 
    item number | equipment | module number | level of significance(text string) | level number(integer)  
    """
    df = pd.read_excel(file,
                        sheet_name=1,
                        header= 1,
                        usecols="A,F",
                        dtype = {0: str , 1: str}
                        )
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df.dropna(how='all') # beta
    return df

def two_columns_ordered(df):
    levels = df[['item_number','level']]#filter usefull column
    #sort by item_number (so I can see the same items stack together)
    levels_ordered = levels.sort_values(by='item_number')
    levels_ordered['Level 1: Critical Parts'] = levels_ordered.level.map({1:1,2:0,3:0}); 
    levels_ordered['Level 2: Useful Parts'] = levels_ordered.level.map({1:0,2:1,3:0}); 
    levels_ordered['Level 3: Complete Parts Inventory'] = levels_ordered.level.map({1:0,2:0,3:1})
    levels_ordered.set_index('item_number')
    df = levels_ordered.groupby(['item_number'], as_index=False)[
    'Level 1: Critical Parts',
    'Level 2: Useful Parts',
    'Level 3: Complete Parts Inventory'
    ].sum()
    return df

def create_three_bool_columns(df):
    df['L1'] = df['Level 1: Critical Parts'].astype(bool).map({True:1,False:0})
    df['L2'] = df['Level 2: Useful Parts'].astype(bool).map({True:1,False:0})
    df['L3'] = df['Level 3: Complete Parts Inventory'].astype(bool).map({True:1,False:0})
    return df

def create_column_possibility(df):
    """create columns: possibility"""
    df.loc[(df.L1==1),'possibility'] = "1"
    df.loc[(df.L2==1),'possibility'] = "2"
    df.loc[(df.L3==1),'possibility'] = "3"
    df.loc[(df.L1==1) & (df.L2==1),'possibility'] = "1|2"
    df.loc[(df.L2==1) & (df.L3==1),'possibility'] = "2|3"
    df.loc[(df.L1==1) & (df.L2==1)& (df.L3==1),'possibility'] = "1|2|3"
    return df      

def create_csv(df, name='db.csv'):
    df.to_csv(name, index=False)
    report = glob('*.xlsm')
    print(f'Task compeleted: -> {name} created ')


def fill_possibility_with_question_mark(df):
    df['possibility'].fillna(0, inplace=True)
    return df

def info_to_print(a , b):
    a, b = len(a) , len(b)
    print(f"""number of excel files : {a + b} (spl:{a}, requisition:{b})""")
    
def main():
    proceed_yes_or_no()
    spls, requisitions = spl_and_requisition_listmaker('.')
    info_to_print(spls, requisitions)
    db = concat(spls)
    db = rows_empty(db)
    db = assign_levels(db)
    db = two_columns_ordered(db)
    db = create_three_bool_columns(db)
    db = create_column_possibility(db)
    db = fill_possibility_with_question_mark(db)
    db_req = requisition_database_builder(requisitions)
    db_req = requisition_database_filter(db, db_req)
    db = pd.concat([db,db_req], sort=False)
    create_csv(db)
    
    
if __name__ == "__main__":
    main()



