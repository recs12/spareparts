import os

# PT User
ACRONYM = os.environ.get('USERNAME')

# INV-PTP-JDE (local)
JDEPATH = r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"

# tempo-files-location (jde_temp, db)
tempo_local = os.path.join(r"T:\tempo", ACRONYM)

# name of temporary jde
temp_jde = r"temporary_jde.csv"

SPL_FRAME = {
    "A2": {"index": "part_number", "header": "Item Number"},
    "B2": {"index": "number", "header": "Number(Drawing)"},
    "C2": {"index": "quantity", "header": "Quantity"},
    "D2": {"index": None , "header": "Equipment"},
    "E2": {"index": "module", "header": "Module"},
    "F2": {"index": "possibility", "header": "Level of significance"},
    "G2": {"index": None, "header": "Category"},
    "H2": {"index": None, "header": "Other Information"},
    "I2": {"index": "unit_of_measure", "header": "UOM"},
    "J2": {"index": "stocking_type", "header": "ST"},
    "K2": {"index": "description_1", "header": "Description 1"},
    "L2": {"index": "description_2", "header": "Description 2"},
    "M2": {"index": "search_text", "header": "Search Text"},
    "N2": {"index": "unit_cost", "header": "Unit Cost"},
    "O2": {"index": None, "header": "Extended Cost"},
    "P2": {"index": "jdelitm", "header": "jdelitm"},
    "Q2": {"index": "description_prp1", "header": "prp1"},
    "R2": {"index": "description_prp2", "header": "prp2"},
    "S2": {"index": "file_name", "header": "file_name"},
    "T2": {"index": "type", "header": "Type"},
    "U2": {"index": "dim", "header": "DIM"},
    "V2": {"index": "comm_class", "header": "Comm Class"},
    "W2": {"index": "supplier", "header": "Supplier"},
    "X2": {"index": "item_pool", "header": "Item Pool"},
}

# Headers in excel file
excel_headers = [SPL_FRAME[i]['header'] for i in SPL_FRAME.keys() if i is not None]

# Dataframes used in each columns
dict_header = {k:v.get('index') for k,v in SPL_FRAME.items() if v.get('index') is not None}

# Colors
orange = (255, 145, 36)  # electric
mauve = (157, 46, 255)   # Items O ou U
blue = (52, 106, 232)    # Items to check
yellow = (235, 247, 133) # background
grey = (183, 185, 188)   # background

# Headers colors of the cells in Excel.
last_columns = list(SPL_FRAME.keys())[-1][0]
headers_bg_hue = {"A1:H1": yellow, f"I1:{last_columns}1": grey}

# File names output
output_1, output_2, output_3  = "template(0).xlsx", "template(1).xlsx", "SPL.xlsx"