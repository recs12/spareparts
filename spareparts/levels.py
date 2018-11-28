#!python3
from glob import glob
import pandas as pd
import os
import xlwings as xw

def loading_spl(path):
        spl = pd.read_excel(path)
        spl.columns = spl.columns.str.strip().str.lower().str.replace(' ', '_')
        spl.item_number = spl.item_number.astype('str')
        spl = spl[['item_number']]
        return spl

def loading_db(path):
        df = pd.read_csv(path)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df.item_number = df.item_number.astype('int')
        df.item_number = df.item_number.astype(str)
        df.item_number = df.item_number.str.strip()
        df = df[['item_number','stat']]
        return df

def on_excel_file(selected_file, datum):
        wb = xw.Book(selected_file)   
        sht = wb.sheets[0]
        sht.range('F2').options(index=False, header=False).value = datum

if __name__ == '__main__':
        spl_path = glob('###*.xlsx')[0]
        spl = loading_spl(spl_path)
        db = loading_db('db.csv')
        l = spl.join(db.set_index('item_number'), on='item_number')
        on_excel_file(spl_path, l['stat'])  
    
    



    