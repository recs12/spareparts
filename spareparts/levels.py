#!python3
from glob import glob
import pandas as pd
import os
import xlwings as xw

def loading_spl(path):
        """load the data from spl list"""
        spl = pd.read_excel(path, sheet_name='Sheet1')
        spl.columns = spl.columns.str.strip().str.lower().str.replace(' ', '_')
        spl.item_number = spl.item_number.astype('str')
        spl = spl[['item_number']]
        return spl

def loading_db(path):
        """load the item-level database"""
        df = pd.read_csv(path, dtype={'possibility': str})
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df.item_number = df.item_number.astype('int')
        df.item_number = df.item_number.astype(str)
        df.item_number = df.item_number.str.strip()
        df.possibility = df.possibility.astype(str)
        df.possibility = df.possibility.str.strip()
        df = df[['item_number','possibility']]
        return df






    