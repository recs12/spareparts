#!python3

import functools
from glob import glob
import os
import pandas as pd
import xlwings as xw
from spareparts.settings.categories import categories 

bin_prp1 = categories['bin']['prp1']
bin_prp2 = categories['bin']['prp2']
electric_prp1 = categories['items_electric']['prp1']
electric_prp2 = categories['items_electric']['prp2']
boulonnerie_prp1 = categories['boulonnerie']['prp1']
plates_prp1 =categories['plates']['prp1']

#load the excel file within a varaible
selected_file = glob('##*.xlsx')[0]

#list of colors RGB code
grey_dark       = (170, 170, 170)       #assemblies
grey            = (150, 150, 150)       #plates
red             = (255, 0, 0)           #boulonnerie
orange          = (255, 145, 36)        #electric
mauve           = (157, 46, 255)        #mauve  Item O ou U
green           = (138, 232, 14)        #green  -   Item avec unité de mesure (pas en EA)
blue            = (52, 106, 232)        #blue  -   Item tjrs à revalider
green           = (48, 203, 232)        #green  -   Item "item number" non conforme
pink           = (232, 86, 113)        #pink  -   bin with all the rest

def colorizing_assemblies(color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        asm_index = d.index[(d['UOM'].isna())&(d['Type']=='asm')].tolist()
                        for row in asm_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_plates(criteria_1, color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.prp1.isin(criteria_1)].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_boulonnerie(criteria_1, color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.prp1.isin(criteria_1)].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_items_electric(criteria_1, criteria_2, color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.prp1.isin(criteria_1) & d.prp2.isin(criteria_2)].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
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
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_FT_RL(color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.UOM.isin(['FT','RL'])].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_MT(color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.UOM.isin(['MT'])].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

def colorizing_bin(criteria_1, criteria_2, color):
        def _outer_wrapper(wrapped_function):
                @functools.wraps(wrapped_function)
                def _wrapper(*args, **kwargs):
                        d,s = wrapped_function(*args, **kwargs)
                        targeted_index = d.index[d.prp1.isin(criteria_1)].tolist()
                        for row in targeted_index:
                                s.range('A2:T2').expand('down').rows[row].color = color
                        return (d,s)
                return _wrapper
        return _outer_wrapper

@colorizing_obsolete_usedup(mauve) 
@colorizing_bin(bin_prp1, bin_prp2 ,pink)
@colorizing_FT_RL(green)
@colorizing_items_electric(electric_prp1, electric_prp2, orange)
@colorizing_boulonnerie(boulonnerie_prp1, red)       
@colorizing_plates(plates_prp1, grey)       
@colorizing_assemblies(grey_dark)
@colorizing_MT(blue)
def on_excel_file(selected_file):
        df = pd.read_excel(selected_file)
        wb = xw.Book(selected_file)   
        sht = wb.sheets[0]
        return (df,sht)

if __name__ == '__main__':
    on_excel_file(selected_file)

#add display ouput for user 
#add progress bar