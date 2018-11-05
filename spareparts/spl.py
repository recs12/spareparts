#!python3
# coding: utf-8

import os
from glob import glob
import logging

import numpy as np
import pandas as pd
import xlwings as xw

JDEPATH = r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"

#filers on prp1
list_prp1 = [
             'Fitting',
             'Metric Fastener',
             'Inch Fastener',
             'Stainless Steel',
             'Steel',
             'Electric Component',
             'Sign & Label'
]

#Excel extracted settings
col = ["Item Number",
        "Drawing",
        "Quantity",
        "Equipment",
        "Module",
        "Level of significance", 
        "Category",
        "Other Information",
        "UOM",
        "ST",
        "Description 1", 
        "Description 2",
        "Search Text",
        "Unit Cost",
        "Extended Cost",
        "jdelitm",
        "prp1", 
        "prp2",
        "file_name",
        "Type"
]

dict_header = {
    'A2':'part_number',
    'C2':'quantity',
    'E2':'module',
    'I2':'stocking_type',
    'K2':'description_1',
    'L2':'description_2',
    'M2':'search_text',
    'N2':'unit_cost',
    'P2':'jdelitm',
    'Q2':'description_prp1',
    'R2':'description_prp2',
    'S2':'file_name',
    'T2':'type'
}

#color cells
color_bg = {
    'I:M' : (235, 247, 133), #yellow
    'A1:C1': (170, 203, 255), #blue
    'D1:H1': (183, 185, 188), #grey
    'I1:M1': (122, 216, 117), #green
    'N1:R1': (122, 100, 100) #red
}

#color legend
color_filters = {
    'I:M' : (235, 247, 133), #bordeau
    'A1:C1': (170, 203, 255), #red
    'D1:H1': (183, 185, 188), #orange
    'I1:M1': (122, 216, 117), #mauve
    'N1:R1': (122, 100, 100) #green
}


logging.basicConfig(filename='sample.log',
                    level=logging.INFO,
                    format= '%(asctime)s : %(name)s : %(message)s')

def timer(func):
    from datetime import datetime as dt
    def inner(data):
        t1= dt.now()
        df = func(data)        
        t2= dt.now()
        logging.info(f"execution time: {(t2- t1).seconds}'s")
        return df
    return inner

#create a timer @decorater for the fonction 
@timer
def extract_jde(location_jde):
    #add a try - except (in case the file is not found)
    print("Link to inventory: ---> {location_jde} \nLoading the JDE Inventory...".format_map(vars()))
    df = pd.read_excel( location_jde ,
                        sheet_name=0,
                        skiprows=[0,1,2,3],
                        usecols="A,C,P,E,H,I,AR,AT,CC",
                        dtype={'Business Unit':int,'Unit Cost':float}
                        )
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df[df.business_unit == 101]
    return df

def extract_data(fichier):
    #add try and except
    df = pd.read_table(fichier,
                    delimiter='\t',
                    skiprows=0, 
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
    print(f"module extracted: -> {module_number}")
    return df

def listing_txt_files(files_path="."):
    for file in os.listdir(files_path):
        if file.endswith(".txt"):
            yield file

def creating_excel(df):
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

def proceed_yes_or_no():
    import sys
    answer = input("Proceed ([y]/n) ?:  ")
    if answer == "y":
        pass
    else:
        sys.exit("Process has stopped.")

def main(location_jde, location_files):
    """manipulation of the date before creating the excel file"""
    #openpyxl may offer some support for speed -> try
    jde = extract_jde(location_jde)
    files_list = [file for file in listing_txt_files(location_files)]
    parts = pd.concat([extract_data(file) for file in files_list], ignore_index=True)
    jde.item_number = jde.item_number.astype(str)
    spl = parts.join(jde.set_index("item_number"), on='jdelitm').sort_values('module')
    ####Filters - prp1 - prp2
    spl = spl[~spl.description_prp1.isin(list_prp1)]
    #filter 111111_P1 .par
    spl= spl[~spl["part_number"].str.contains(r"\d{6}_P?\d{1}").values]
    #create a column part type
    spl['type'] = spl.file_name.str.split('.').str[-1].str.strip()
    #filter asm without UOM
    spl = spl[~((spl['stocking_type'].isna())&(spl['type']=='asm'))]
    ####Excel file creation 
    creating_excel(spl) 
    
if __name__ == '__main__':
    main(JDEPATH ,".")
    # main("INV-PTP-JDE.xlsx")

#canei
#remplace the letters variable by meaningfull name
#REFACTOR
#add docstring
#raise exception inside fouctions
#logging file whitout root:
#progress bar
