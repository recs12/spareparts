#!python3
# -*- coding: utf-8 -*-

import sys
import os
from glob import glob
from pt_resources.toolkit import check_platform

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
    check_platform()
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
    spl, garbage, elec, nuts, plates, asm  = strain(spl, garbage)
    TABS = {
        'nuts': nuts,
        'asm': asm,
        'plates': plates,
        'elec': elec,
        'garbage': garbage,
        'spl': spl,
    }
    line_number_display(spl, garbage, plates, elec, asm, nuts)
    creating_excel(TABS, output_1)
    editing_excel(output_1, output_2)
    coloring_excel(TABS , output_2, output_3) #ADD TAB NUTS IN TABS VARIABLE IN SETTINGS

if __name__ == '__main__':
    generating_spl(JDEPATH, JDE_TEMP,".")

#TODO: add jde data field to compare report "difference.txt". (merge function)
#TODO: add documentation code (pycco)
#TODO: merge autofilter + alignment_column_significance step
#TODO: [BUG] clean double line: 19 letters max the next line is to delete. IF partnumber letters =19 then delete following line if plenty of blanks

