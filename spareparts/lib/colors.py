#!python3
# -*- coding: utf-8 -*-

import functools
from glob import glob
import os
import pandas as pd
import xlwings as xw
from spareparts.lib.settings import *

#list of colors RGB code
orange = (255, 145, 36)        #electric
mauve  = (157, 46, 255)        #mauve  Item O ou U
blue   = (52, 106, 232)        #blue  -   Item tjrs à revalider

def colorizing_items_electric(prp1, color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.prp1.isin(prp1)].tolist()
                        for row in targeted_index:
                                cellule = f"A{row+2}:U{row+2}" # number 2 added for compensate lapse in excel file
                                s.range(cellule).color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_obsolete_usedup(color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.ST.isin(['O','U'])].tolist()
                        for row in targeted_index:
                                cellule = f"J{row+2}" # number 2 added for compensate lapse in excel file
                                s.range(cellule).color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_MT_FT_RL(color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.UOM.isin(['MT','FT','RL'])].tolist()
                        for row in targeted_index:
                                cellule = f"I{row+2}" # number 2 added for compensate lapse in excel file
                                s.range(cellule).color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

@colorizing_items_electric(electric_prp1, orange)
@colorizing_obsolete_usedup(mauve)
@colorizing_MT_FT_RL(blue)
def extraction(file_name , workbook , sht_name ):
        df = pd.read_excel(file_name , sheet_name=sht_name)
        sht = workbook.sheets[sht_name]
        return (df,sht)

def add_colors(selected_file, sheet_spl ):
        wb = xw.Book(selected_file)
        extraction(selected_file, wb ,sheet_spl)
        return wb

def color_coding(args, selected_file, new_file):
        for tab in args:
                wb = add_colors(selected_file, tab)
        wb.save(new_file)



