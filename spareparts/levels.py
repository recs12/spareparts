#!python3
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

list_of_spl = glob('*SPL*.xlsm')
print(list_of_spl)

dk = {'Level 3: Complete Parts Inventory': 3,
 'Level 2: Useful Parts': 2,
 'Level 1: Critical Parts': 1,
 '1': 1,
 '2': 2,
 '3': 3}

def extract_levels(file):
    """extraction of the data from the excel SPL file
    the excel file must have <SPL> written in the filename
    extracted : 
    item number | equipment | module number | level of significance(text string) | level number(integer)  
    """
    df = pd.read_excel(file,
                        sheet_name=1,
                        header= 1,
                        usecols="A,D,E,F")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

#merge the data of all excel file the same dataframe with pandas
files_list = (file for file in list_of_spl)
levels = pd.concat([extract_levels(file) for file in files_list], ignore_index=True)
#filter the empty rows
levels = levels[levels.item_number.notnull()]
#create a new column with the level for each row
levels['level'] = levels.level_of_significance.map(dk, na_action=None)
#create exvel file output
levels.to_csv('levels.csv')
            



