import os
import pandas as pd
import numpy as np
import xlwings as xw
from spareparts.lib.settings import *

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
        # df.item_number = df.item_number.astype('int')
        df.item_number = df.item_number.astype(str)
        df.item_number = df.item_number.str.strip()
        df.possibility = df.possibility.astype(str)
        df.possibility = df.possibility.str.strip()
        df = df[['item_number','possibility']]
        return df

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
                        usecols="A,C,P,E,H,I,K,O,AR,AT,CB" ,
                        dtype={'Business Unit':int,'Unit Cost': float }
                        )
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df[df.business_unit == 101]
    print(df.columns)
    return df

def load_jde_data(location_jde, path_to_temp):
    """"""
    if os.path.exists(path_to_temp):
        answer = input("Do you want to load the temporary jde? (fast but not recommended) \n Proceed ([y]/n) ?:")
        if answer in ['yes','y','YES','Y']:
            jde_temp = pd.read_csv(path_to_temp)
            return jde_temp
        else:
            sys.exit()
    else:
        jde_data = extract_jde(location_jde)
        jde_data.to_csv(path_to_temp, index=False)
        return jde_data

def extract_data(fichier):
    """"""
    #add try and except
    df = pd.read_csv(fichier,
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
    df = replacing_C01(df)
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
    """fill the tabs in excel file with the dataframes"""
    wb = xw.Book()    # this will create a new workbook
    sht = wb.sheets[0] #skip the Sheet1 and create spl within a loop for all tab
    sht.range('A1').value = excel_headers #insert headers 
    #color cells
    sht.range('A1:R1').api.Font.Bold = True #bold headers
    for rang,color in headers_bg_hue.items():
        xw.Range(rang).color = color
    for colum,data in dict_header.items():
        sht.range(colum).options(index=False, header=False).value = df[data]
    sht.autofit()
    sht_garb = wb.sheets.add('garbage')
    sht_garb.range('A1').value = excel_headers
    sht_nuts = wb.sheets.add('_nuts')
    sht_nuts.range('A1').value = excel_headers
    #color cells
    sht_garb.range('A1:R1').api.Font.Bold = True #bold first row
    for rang,color in headers_bg_hue.items():
        xw.Range(rang).color = color
    for colum,data in dict_header.items():
        sht_garb.range(colum).options(index=False, header=False).value = df_removed[data]
    sht_garb.autofit()
    wb.save(given_name_xlsx)
    wb.close()

def joining_spl_jde(jde, parts):
    """transform the jde column to string format
    join the parts documents with the jde on jdelitm column
    and sort it on column:module
    """
    jde.item_number = jde.item_number.astype(str)
    spl = parts.join(jde.set_index("item_number"), on='jdelitm').sort_values('module')
    # spl.to_csv('earliest_spl.csv', index=False) ####test to remove
    return spl

def creating_part_type_column(spl):
    """create a column type --> .par .psm .asm"""
    spl['type'] = spl.file_name.str.split('.').str[-1].str.strip()
    return spl

def creating_drawing_number_column(spl, jde):
    """create a column bool: drawing number --> TRUE/FALSE"""
    list_of_drawings = jde["drawing_number"].dropna().tolist()
    spl['part_number'] = spl['part_number'].str.strip()
    spl['drawing'] = spl.part_number.isin(list_of_drawings)
    return spl

def line_number_display(spl, garbage):
    print("-----------------------------\n"
        f"shape spl:\t{spl.shape[0]}\n"
        f"shape garbage:\t{garbage.shape[0]}"
        "\n-----------------------------")

def replacing_C01(spl):
    """
        Replacing 123456_C01 to 123456, those are different
        configs of belt refering to the same item number in the JDE.
    """
    pat = r"(?P<number>\d{6})(?P<suffixe>_C\d{2})"
    repl = lambda m:m.group('number')
    spl['part_number'] = spl['part_number'].str.replace(pat, repl)
    return spl