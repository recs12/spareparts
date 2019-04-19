#!python3
# -*- coding: utf-8 -*-

import sys
import os
from glob import glob
import pandas as pd
from spareparts.lib.formatting import *
from spareparts.lib.dispatch import *
from spareparts.lib.settings import *
from spareparts.lib.toolkit import *
from spareparts.lib.filtrate import strain
from spareparts.lib.colors import *

DB = os.path.join(temp_path, levels_db)
JDE_TEMP = os.path.join(temp_path, temp_jde)

def generating_spl(location_jde, location_jde_temp, location_files):
    """manipulation of the date before creating the excel file"""
    proceed_yes_or_no()
    jde = load_jde_data(location_jde, location_jde_temp)
    garbage = pd.DataFrame()
    files_list = (file for file in listing_txt_files(location_files))
    parts = pd.concat([extract_data(file) for file in files_list], ignore_index=True)
    spl = joining_spl_jde(jde, parts)
    db = loading_db(DB)
    spl = spl.join(db.set_index('item_number'), on='jdelitm')
    spl = creating_part_type_column(spl)
    spl = creating_drawing_number_column(spl, jde)
    spl, garbage = strain(spl, garbage)
    line_number_display(spl, garbage)
    creating_excel(spl, garbage ,output_1)
    autofilter(output_1, output_2)
    alignment_column_significance(output_2, output_3)
    color_coding(TABS , output_3, output_4)

if __name__ == '__main__':
    generating_spl(JDEPATH, JDE_TEMP,".")

#TODO: change all: garbage => garb
#TODO: generate a report of the transfrerts in a folder called "report"
#TODO: integrate the coloring in the spl.py entry-point
#TODO: color the missing items in excel file for check
#TODO: add a location for db.py and temporary_jde in C:
#TODO: add instructions in the code and in the excel file
#TODO: add replace.py file that replace some item in the SPL.
#TODO: rewrite the app in OO way.
#TODO: add jde data field to compare report "difference.txt". (merge function)
#TODO: add documentation code (pycco)
#TODO: merge autofilter + alignment_column_significance step
