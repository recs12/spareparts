import pandas as pd
import os
from glob import glob
from spareparts.spl import extract_jde

JDEPATH = r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"

def selecting_file():
    """identifying the file to pick"""
    file_excel = glob('#*.xlsm')[0] #we got a list type 
    return file_excel

def importing_excel(excel):
    df = pd.read_excel(excel)
    return df

def cmd_display():
    print(f"{function name} \t done")

def creating_excel(excel):
    pass
    

#import jde_temporary
#if not in folder import jde
#extract karl excel data
#add the prp1 columns
#download new file _extra.xlsm

if __name__ == '__main__':
    #jde = extract_jde(JDEPATH)
    importing_excel(selecting_file())
    