import pandas as pd
import xlwings as xw
from spareparts.lib.settings import *
import functools

def keep_item(regx):
    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garb, reloc = wrapped_function(*args, **kwargs)
            reloc = garb[garb.part_number.str.contains(regx, na=False, regex=True)]
            garb = garb[~garb.part_number.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, reloc], ignore_index=True, sort=False)
            return (spl, garb, reloc)
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
    spl= spl[~spl["part_number"].str.contains(r"\d{6}_[P|A]?\d{1}").values]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)

#asm_exceptions = r"EEG58C6000A-.*"
@keep_item('EEG58C6000A-.*')
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

def trash_prp1(spl, garbage, prp1=[]):
    """prp1, prp2"""
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

