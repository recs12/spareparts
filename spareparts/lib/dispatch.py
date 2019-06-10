import pandas as pd
import xlwings as xw
import functools
from loguru import logger
from spareparts.lib.settings import *

def special_partnumber(regx):
    """decorator"""
    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[assem.part_number.str.contains(regx, na=False, regex=True)]
            assem = assem[~assem.part_number.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)
        return _wrapper
    return _outer_wrapper

def special_description_1(regx):
    """decorator"""
    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[assem.description_1.str.contains(regx, na=False, regex=True)]
            assem = assem[~assem.description_1.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)
        return _wrapper
    return _outer_wrapper

def special_description_2(regx):
    """decorator"""
    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[assem.description_2.str.contains(regx, na=False, regex=True)]
            assem = assem[~assem.description_2.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)
        return _wrapper
    return _outer_wrapper

def adjust_significance_notnull(spl, garbage):
    """relocate the significance is not nan"""
    relocate = garbage[garbage.possibility.notna()]
    garbage = garbage[~garbage.possibility.notna()]
    spl = pd.concat([spl, relocate], ignore_index=True)
    return (spl, garbage, relocate)

def trash_parts_ending_P1_or_A1(spl, garbage):
    """filter --> number_P1.par  & number_A1.par"""
    relocate= spl[spl["part_number"].str.contains(r"\d{6}_[P|A]?\d{1}").values]
    spl= spl[~spl["part_number"].str.contains(r"\d{6}[_|-][P|A]?\d{1}").values]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

@special_partnumber('PT0038724')
@special_partnumber('EEG58C6000A-.*')
def trash_assemblies(spl, garbage):
    """filter -> ASSEMBLY (with exceptions)"""
    relocate = spl[ (spl.unit_of_measure.isna()) & (spl.type =='asm') ]
    spl = spl[ ~( (spl.unit_of_measure.isna()) & (spl.type =='asm') )]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

def trash_robot(spl, garbage, criteres=['LR Mate']):
    """robot -> garbage"""
    relocate = spl[spl.type.isin(criteres)]
    spl = spl[~spl.type.isin(criteres)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

@special_partnumber('214938')
@special_partnumber('122857')
@special_partnumber('24300030')
@special_partnumber('122896')
def trash_description(spl, garbage, keyword, description="description_1"):
    """description_1 OR description_2"""
    relocate = spl[spl[description].str.contains(keyword, na=False, regex=True)]
    spl = spl[~spl[description].str.contains(keyword, na=False, regex=True)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

def trash_prp(spl, garbage, prp1=[], prp2=[]):
    """prp1, prp2"""
    relocate = spl[spl.description_prp1.isin(prp1) & spl.description_prp2.isin(prp2)]
    spl = spl[~(spl.description_prp1.isin(prp1) & spl.description_prp2.isin(prp2))]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

@special_description_2(r"Retaining Ring")
@special_description_2(r"Seal")
@special_description_2(r"Door&Panel, Hardware&Furniture")
@special_description_2(r"Coupling, Bushing & Shaft Acc.")
@special_description_2(r"Door&Panel, Hardware&Furniture")
@special_description_2(r"Spring, Shock & Bumper")
@special_description_2(r'.*?\bBARB\b.*?\bNYLON\b.*?') #regex: line with both words BARB and bNYLON.
@special_description_1('BFR')
@special_description_1('BUMPER')
def trash_prp1(spl, garbage, prp1=[]):
    """prp1"""
    relocate = spl[spl.description_prp1.isin(prp1)]
    spl = spl[~spl.description_prp1.isin(prp1)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

def trash_item_number(spl, garbage, list_parts):
    """filter -> parts inside the gripper"""
    relocate = spl[spl.part_number.isin(list_parts)]
    spl = spl[~spl.part_number.isin(list_parts)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

def trash_file_name(spl, garbage, keyword):
    """filter -> par in /file_name/"""
    relocate = spl[spl.file_name.str.contains(keyword, na=False, regex=True)]
    spl = spl[~spl.file_name.str.contains(keyword, na=False, regex=True)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

