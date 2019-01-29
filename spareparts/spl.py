#!python3
# -*- coding: utf-8 -*-
"""A module-level docstring
Create a sparepart list from files, download from solidedge ST7.
"""

# import click
import os
import sys
from glob import glob
import logging
import numpy as np
import pandas as pd
import xlwings as xw
from spareparts.parameters import *
from spareparts.levels import *

boulonnerie_prp1 = categories['boulonnerie']['prp1']
plates_prp1 = categories['plates']['prp1']
electric_prp1 = categories['items_electric']['prp1']
electric_prp2 = categories['items_electric']['prp2']
bin_prp1 = categories['bin']['prp1']

def timer(func):
    """"""
    from datetime import datetime as dt
    def inner(data):
        t1= dt.now()
        df = func(data)
        t2= dt.now()
        print(f"JDE loading time:\t{(t2- t1).seconds}'s")
        return df
    return inner

def proceed_yes_or_no():
    "ask user to resume the program"
    print(f"Run: {__file__}")
    answer = input("Proceed ([y]/n) ?:  ")
    if answer in ['yes','y','YES','Y']:
        pass
    else:
        sys.exit("Process has stopped.")

@timer
def extract_jde(location_jde):
    """"""
    #add a try - except (in case the file is not found)
    print("Link to inventory: ---> {location_jde} \nLoading the JDE Inventory...".format_map(vars()))
    df = pd.read_excel( location_jde ,
                        sheet_name=0,
                        skiprows=[0,1,2,3],
                        usecols="A,C,P,E,H,I,O,AR,AT,CB",
                        dtype={'Business Unit':int,'Unit Cost': float }
                        )
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df[df.business_unit == 101]
    return df

def load_jde_data(location_jde):
    """"""
    if os.path.exists("temporary_jde.csv"):
        answer = input("Do you want to load the temporary jde? (fast but not recommended) \n Proceed ([y]/n) ?:")
        if answer in ['yes','y','YES','Y']:
            jde_temp = pd.read_csv("temporary_jde.csv")
            return jde_temp
        else:
            sys.exit()
    else:
        jde_data = extract_jde(location_jde)
        jde_data.to_csv("temporary_jde.csv")
        return jde_data

def extract_data(fichier):
    """"""
    #add try and except
    df = pd.read_table(fichier,
                    delimiter='\t',
                    skiprows=[0,2], 
                    header=1,
                    names= ["Part Number","Revision","DSC_A", "JDELITM","DIM","Quantity", "File Name"],
                    index_col=False,             
                    encoding='latin3', 
                    error_bad_lines=False,
                    na_values="-"
                   )
    #clean the columns
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['jdelitm'] = df['jdelitm'].str.strip()
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerse')
    df = df.groupby(['part_number','revision','dsc_a','jdelitm','file_name'], as_index=False)['quantity'].sum()
    df = df.replace(r'^-?\s+$', np.nan ,regex=True)
    df = df.dropna(subset=['part_number','jdelitm'])
    #give the module number
    module_number = os.path.splitext(os.path.basename(fichier))[0]
    df['module'] = module_number
    print(f" [+][\t{module_number}\t]")
    return df

def listing_txt_files(files_path="."):
    """"""
    for file in os.listdir(files_path):
        if file.endswith(".txt"):
            yield file

def creating_excel(df, df_removed, given_name_xlsx):
    """"""
    wb = xw.Book()    # this will create a new workbook
    sht = wb.sheets[0]
    sht.range('A1').value = col
    #color cells
    sht.range('A1:R1').api.Font.Bold = True #bold first row
    for rang,color in color_bg.items():
        xw.Range(rang).color = color 
    for colum,data in dict_header.items():
        sht.range(colum).options(index=False, header=False).value = df[data]
    sht.autofit()
    sht2 = wb.sheets.add('garbage')
    sht2.range('A1').value = col
    #color cells
    sht2.range('A1:R1').api.Font.Bold = True #bold first row 
    for rang,color in color_bg.items():
        xw.Range(rang).color = color 
    for colum,data in dict_header.items():
        sht2.range(colum).options(index=False, header=False).value = df_removed[data]
    sht2.autofit()
    wb.save(given_name_xlsx)


def joining_spl_jde(jde, parts):
    """transform the jde column to string format
    join the parts documents with the jde on jdelitm column
    and sort it on column:module
    """
    jde.item_number = jde.item_number.astype(str)
    spl = parts.join(jde.set_index("item_number"), on='jdelitm').sort_values('module')
    return spl

def creating_part_type_column(spl):
    """create a column type --> .par .psm .asm"""
    spl['type'] = spl.file_name.str.split('.').str[-1].str.strip()
    return spl

def filtering_part_P1_or_A1_format(spl):
    """filter --> number_P1.par  & number_A1.par"""
    spl= spl[~spl["part_number"].str.contains(r"\d{6}_[P|A]?\d{1}").values]
    return spl

def filtering_nuts(data, criteres=boulonnerie_prp1):
    """filter -> nuts"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_assemblies(data):
    """filter -> ASSEMBLY"""
    data_remaining = data[~((data['unit_of_measure'].isna())&(data['type']=='asm'))]
    data_removed = data[(data['unit_of_measure'].isna())&(data['type']=='asm')]
    return (data_remaining , data_removed)

def filtering_plates(data, criteres=plates_prp1):
    """filter -> plates"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_electric(data, c1=["Electric Component"], c2=["Cable Tray & Cable Carrier","Conduits & fittings"]):
    """filter -> electric"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_bin(data, criteres=bin_prp1):
    """filter -> bin"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_robot(data, criteres=['LR Mate']):
    """filter -> robot"""
    data_remaining = data[~data.type.isin(criteres)]
    data_removed = data[data.type.isin(criteres)]
    return (data_remaining , data_removed)


def generating_spl(location_jde, location_files):
    """manipulation of the date before creating the excel file"""
    proceed_yes_or_no()
    jde = load_jde_data(location_jde)
    files_list = (file for file in listing_txt_files(location_files))
    parts = pd.concat([extract_data(file) for file in files_list], ignore_index=True)
    spl = joining_spl_jde(jde, parts)
    db = loading_db('db.csv') 
    spl = spl.join(db.set_index('item_number'), on='jdelitm')
    spl = creating_part_type_column(spl)
    
    ###filters###
    spl = filtering_part_P1_or_A1_format(spl)
    spl , nuts = filtering_nuts(spl)
    spl , assemblies = filtering_assemblies(spl)
    spl , plates = filtering_plates(spl);print(filtering_plates.__doc__)
    spl , elec = filtering_electric(spl);print(filtering_electric.__doc__)
    spl , divers = filtering_bin(spl)
    spl , robot = filtering_robot(spl)
    #############

    garbage = pd.concat([nuts, assemblies, plates, elec, divers, robot], ignore_index=True).sort_values('module',ascending=True)
    creating_excel(spl, garbage ,'auto.xlsx') 
    print(f"Task completed")
    
if __name__ == '__main__':
    generating_spl(JDEPATH ,".")

