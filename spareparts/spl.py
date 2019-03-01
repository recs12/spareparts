#!python3
# -*- coding: utf-8 -*-
"""A module-level docstring
Create a sparepart list from files, download from solidedge ST7.
"""

# import click
import os
import sys
from glob import glob
import logging
import numpy as np
import pandas as pd
import xlwings as xw
from spareparts.parameters import *
from spareparts.filters import autofilter
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Alignment



boulonnerie_prp1 = categories['boulonnerie']['prp1']
plates_prp1 = categories['plates']['prp1']
electric_prp1 = categories['items_electric']['prp1']
electric_prp2 = categories['items_electric']['prp2']
bin_prp1 = categories['bin']['prp1']

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

def load_jde_data(location_jde):
    """"""
    if os.path.exists("temporary_jde.csv"):
        answer = input("Do you want to load the temporary jde? (fast but not recommended) \n Proceed ([y]/n) ?:")
        if answer in ['yes','y','YES','Y']:
            jde_temp = pd.read_csv("temporary_jde.csv")
            return jde_temp
        else:
            sys.exit()
    else:
        jde_data = extract_jde(location_jde)
        jde_data.to_csv("temporary_jde.csv", index=False)
        return jde_data

def extract_data(fichier):
    """"""
    #add try and except
    df = pd.read_table(fichier,
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
    """"""
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
    sht2 = wb.sheets.add('garbage')
    sht2.range('A1').value = col
    #color cells
    sht2.range('A1:R1').api.Font.Bold = True #bold first row 
    for rang,color in color_bg.items():
        xw.Range(rang).color = color 
    for colum,data in dict_header.items():
        sht2.range(colum).options(index=False, header=False).value = df_removed[data]
    sht2.autofit()
    wb.save(given_name_xlsx)


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

def alignment_column_significance(file_name):
    new_name = 'auto_with_filters_aligned.xlsx'
    wb = load_workbook(file_name)
    for sheet in wb.sheetnames: 
        ws = wb[sheet]
        significance_column = ws['F']
        for cell in significance_column:
            cell.alignment = Alignment(horizontal='center') 
    print(f"excel file created: {new_name}")
    return wb.save()

#*****************filters*********************

def filtering_part_P1_or_A1_format(spl):
    """filter --> number_P1.par  & number_A1.par"""
    spl= spl[~spl["part_number"].str.contains(r"\d{6}_[P|A]?\d{1}").values]
    return spl

def filtering_nuts(data, criteres=boulonnerie_prp1):
    """filter -> nuts"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_assemblies(data, asm_exceptions = r"EEG58C6000A-.*"):
    """filter -> ASSEMBLY (with exceptions)"""
    data_remaining = data[ ~( (data.unit_of_measure.isna()) & (data.type =='asm') & (~data.part_number.str.contains( asm_exceptions  , regex=True)) )]
    data_removed = data[ (data.unit_of_measure.isna()) & (data.type =='asm') & (~data.part_number.str.contains( asm_exceptions  , regex=True))]
    return (data_remaining , data_removed)

def filtering_plates(data, criteres=plates_prp1):
    """filter -> plates"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_electric(data, c1=["Electric Component"], c2=["Cable Tray & Cable Carrier","Conduits & fittings","Enclosures","Sensors","Lights & bulbs","Switches","General hardware"]):
    """filter -> electric"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_bin(data, criteres=bin_prp1):
    """filter -> bin"""
    data_remaining = data[~data.description_prp1.isin(criteres)]
    data_removed = data[data.description_prp1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_robot(data, criteres=['LR Mate']):
    """filter -> robot"""
    data_remaining = data[~data.type.isin(criteres)]
    data_removed = data[data.type.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_grommet(data, c1=["Mechanical Component"], c2=["Nut & Washer"]):
    """filter -> grommet"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_factory_furniture(data, c1=["Factory Furniture"], c2=["Tape"]):
    """filter -> Factory Furniture - Tape"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_industrial(data, c1=["Industrial Engine"], c2=["Engine Parts"]):
    """filter -> Industrial Engine - Engine Parts"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_pneumatic(data, jde_numbers =['216078', '216120', '216081', '162463']):
    """filter -> 216078, 216120, 216081, 162463 """
    data_remaining = data[~data.jdelitm.isin(jde_numbers)]
    data_removed = data[data.jdelitm.isin(jde_numbers)]
    return (data_remaining , data_removed)

def filtering_pneu_frl(data):
    """filter -> PNEU.F.R.L. in /description_1/ """
    data_remaining = data[~data["description_1"].str.contains(r"PNEU\.F\.R\.L", na=False, regex=True)]
    data_removed = data[data["description_1"].str.contains(r"PNEU\.F\.R\.L", na=False , regex=True)]
    return (data_remaining , data_removed)

def filtering_pneu_manifold(data):
    """filter -> manifold in /description_1/ """
    data_remaining = data[~data["description_1"].str.contains(r"PNEU.VALVE\sMANIFOLD\s[\d/\d\:\d{2}|\d\:\d{2}]", na=False, regex=True)]
    data_removed = data[data["description_1"].str.contains(r"PNEU.VALVE\sMANIFOLD\s[\d/\d\:\d{2}|\d\:\d{2}]", na=False , regex=True)]
    return (data_remaining , data_removed)

def filtering_par(data, criteres=['par']):
    """filter -> par in /file_name/"""
    data_remaining = data[~data.file_name.isin(criteres)]
    data_removed = data[data.file_name.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_timing_belt_sheave(data, criteres=['TIMING BELT SHEAVE']):
    """filter -> timing_belt_sheave in description_1"""
    data_remaining = data[~data.description_1.isin(criteres)]
    data_removed = data[data.description_1.isin(criteres)]
    return (data_remaining , data_removed)

def filtering_cable_carrier(data, c1=["Mechanical Component"], c2=["Cable Tray & Cable Carrier"]):
    """filter -> cable carrier"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_motor_shrink_disk(data, c1=["Mechanical Component"], c2=["Clutch, Brake & Torque Limiter"]):
    """filter -> motor shrink disk"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_gearmotor_servomotor(data, c1=["Mechanical Component"], c2=["Gear Motor & Motor"]):
    """filter -> gearmotor & servomotor"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_gearbox(data, c1=["Mechanical Component"], c2=["Gearbox, Gear, Rack & Pinion"]):
    """filter -> gearbox"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_clamps(data, key_word=["CLAMP;TRANSPORT UNIT"]):
    """filter -> CLAMP;TRANSPORT UNIT"""
    data_remaining = data[~data.description_2.isin(key_word)]
    data_removed = data[data.description_2.isin(key_word)]
    return (data_remaining , data_removed)

def filtering_quincaillery(data, c1=["Mechanical Component"], c2=["Quincaillery"]):
    """filter -> quincaillery"""
    data_remaining = data[~(data.description_prp1.isin(c1) & data.description_prp2.isin(c2))]
    data_removed = data[data.description_prp1.isin(c1) & data.description_prp2.isin(c2)]
    return (data_remaining , data_removed)

def filtering_parts_inside_gripper(data, list_parts=contents_of_gripper):
    """filter -> parts inside the gripper"""
    data_remaining = data[~data.part_number.isin(list_parts)]
    data_removed = data[data.part_number.isin(list_parts)]
    return (data_remaining , data_removed)

#**************************end filters ***************************************

def generating_spl(location_jde, location_files):
    """manipulation of the date before creating the excel file"""
    proceed_yes_or_no()
    jde = load_jde_data(location_jde)
    files_list = (file for file in listing_txt_files(location_files))
    parts = pd.concat([extract_data(file) for file in files_list], ignore_index=True)
    spl = joining_spl_jde(jde, parts)
    db = loading_db('db.csv') 
    spl = spl.join(db.set_index('item_number'), on='jdelitm')
    spl = creating_part_type_column(spl)
    spl = creating_drawing_number_column(spl, jde)
    ###filters###
    spl = filtering_part_P1_or_A1_format(spl);print(filtering_part_P1_or_A1_format.__doc__)
    spl , nuts = filtering_nuts(spl);print(filtering_nuts.__doc__)
    spl , assemblies = filtering_assemblies(spl);print(filtering_assemblies.__doc__)
    spl , plates = filtering_plates(spl);print(filtering_plates.__doc__)
    spl , elec = filtering_electric(spl);print(filtering_electric.__doc__)
    spl , divers = filtering_bin(spl);print(filtering_bin.__doc__)
    spl , robot = filtering_robot(spl);print(filtering_robot.__doc__)
    spl , grommet = filtering_grommet(spl);print(filtering_grommet.__doc__)
    spl , factory_furniture = filtering_factory_furniture(spl);print(filtering_factory_furniture.__doc__)
    spl , industrial = filtering_industrial(spl);print(filtering_industrial.__doc__)
    spl , pneumatic = filtering_pneumatic(spl);print(filtering_pneumatic.__doc__)
    spl , pneu_frl = filtering_pneu_frl(spl);print(filtering_pneu_frl.__doc__)
    spl , pneu_manifold = filtering_pneu_manifold(spl);print(filtering_pneu_manifold.__doc__)
    spl , par = filtering_par(spl);print(filtering_par.__doc__)
    spl , timing_belt_sheave = filtering_timing_belt_sheave(spl);print(filtering_timing_belt_sheave.__doc__)
    spl , cable_carrier = filtering_cable_carrier(spl);print(filtering_cable_carrier.__doc__)
    spl , motor_shrink_disk = filtering_motor_shrink_disk(spl);print(filtering_motor_shrink_disk.__doc__)
    spl , gearmotor_servomotor = filtering_gearmotor_servomotor(spl);print(filtering_gearmotor_servomotor.__doc__)
    spl , gearbox = filtering_gearbox(spl);print(filtering_gearbox.__doc__)
    spl , clamps = filtering_clamps(spl);print(filtering_clamps.__doc__)
    spl , quincaillery = filtering_quincaillery(spl);print(filtering_quincaillery.__doc__)
    spl , inside_gripper = filtering_parts_inside_gripper(spl);print(filtering_parts_inside_gripper.__doc__)
    #############
    groupe_to_concat = [nuts, assemblies, plates, elec, divers, robot, grommet, factory_furniture,industrial, pneumatic, par, timing_belt_sheave, cable_carrier, motor_shrink_disk, gearmotor_servomotor, gearbox, clamps, quincaillery, pneu_frl, pneu_manifold, inside_gripper]
    garbage = pd.concat(groupe_to_concat , ignore_index=True).sort_values('module',ascending=True)
    print("-----------------------------\n"
        f"shape spl:\t{spl.shape[0]}\n"
        f"shape garbage:\t{garbage.shape[0]}"
        "\n-----------------------------")
    creating_excel(spl, garbage ,'auto.xlsx')
    autofilter('auto.xlsx')
    alignment_column_significance('auto_with_filters.xlsx')
    print(f"excel file created: auto.xlsx")
    
if __name__ == '__main__':
    generating_spl(JDEPATH ,".")

