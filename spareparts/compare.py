#! python3
# 2019-03-27 by recs
# ===check the current owner of type licenses===

import pandas as pd
import os
from spareparts.lib.settings import tempo_local, temp_jde

index_manual = ['How to fill fileds in the Data Tab', 'Unnamed: 1', 'Unnamed: 2']

index_auto = ['Item Number',
    'Number(Drawing)',
    'Quantity',
    'Equipment',
    'Module',
    'Level of significance',
    'Category',
    'Other Information',
    'UOM',
    'ST',
    'Description 1',
    'Description 2',
    'Search Text',
    'Unit Cost',
    'Extended Cost',
    'jdelitm',
    'prp1',
    'prp2',
    'file_name',
    'Type',
    'DIM',
    'Comm Class',
    'Supplier',
    'Item Pool'
]


# Path to temporary_jde.csv in windows OS.
if os.path.join(tempo_local, temp_jde):
    path_to_jde = os.path.join(tempo_local, temp_jde)
else:
    print("the temporary jde file is not in the TEMPO of RECS")


def extract_items_auto(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name="spl", header=0, usecols="A", dtype={0: str})
    data["Item Number"] = data["Item Number"].str.strip()
    data = data.dropna(how="all")
    serie = pd.Series(data["Item Number"])
    serie = serie.unique().tolist()
    return set(serie)


def extract_items_manual(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name="Data", header=0, usecols="A", dtype={0: str})
    data.columns = ["items"]
    data["items"] = data["items"].str.strip()
    data = data.dropna(how="all")
    serie = pd.Series(data["items"])
    serie = serie.unique().tolist()[1:]
    return set(serie)


def parsing_items(name_file):
    name_file = str(name_file)
    if pd.read_excel(name_file).columns.tolist() == index_manual:
        return extract_items_manual(name_file)
    elif pd.read_excel(name_file).columns.tolist() == index_auto:
        return extract_items_auto(name_file)
    else:
        print(
            f"[WARNING] : {name_file} : Wrong file format, only auto or standard sparepart list."
        )


def joining_spl_jde(jde, parts):
    jde.item_number = jde.item_number.astype(str)
    spl = parts.join(jde.set_index("item_number"), on="item_number")
    return spl


def load_jde_data():
    jde_temp = pd.read_csv(path_to_jde)
    return jde_temp


def delta(spl1, spl2):
    return sorted(list(parsing_items(spl1) - parsing_items(spl2)))


def differences(spl1, spl2):
    #TODO: Check the name of files to compare.
    df = pd.DataFrame(delta(spl1, spl2), columns=["item_number"])
    jde = load_jde_data()
    parts = joining_spl_jde(jde, df)
    parts.to_csv("differences.csv", index=False)
    # TODO: Add message excecution
    # TODO: [INFO] same files.
    # TODO: [INFO] diff.csv already exist.



# TODO: Can compare pneumatic list option
