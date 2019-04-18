#!python3
# -*- coding: utf-8 -*-

import sys
from glob import glob
import pandas as pd
from spareparts.lib.formatting import *
from spareparts.lib.dispatch import *
from spareparts.lib.settings import *
from spareparts.lib.toolkit import *
from spareparts.lib.filtrate import strain

def generating_spl(location_jde, location_files):
    """manipulation of the date before creating the excel file"""
    proceed_yes_or_no()
    jde = load_jde_data(location_jde)
    garbage = pd.DataFrame()
    files_list = (file for file in listing_txt_files(location_files))
    parts = pd.concat([extract_data(file) for file in files_list], ignore_index=True)
    spl = joining_spl_jde(jde, parts)
    db = loading_db('db.csv')
    spl = spl.join(db.set_index('item_number'), on='jdelitm')
    spl = creating_part_type_column(spl)
    spl = creating_drawing_number_column(spl, jde)
    spl, garbage = strain(spl, garbage)
    line_number_display(spl, garbage)
    creating_excel(spl, garbage ,'auto.xlsx')
    autofilter('auto.xlsx')
    alignment_column_significance('auto_with_filters.xlsx')

if __name__ == '__main__':
    generating_spl(JDEPATH ,".")

#TODO: Set in SETTINGS file the temporary files location like Temp
