import os

# tempo-files-location (jde_temp, db)
tempo_local = r"T:\tempo\recs"


# name of temporary jde
temp_jde = r"temporary_jde.csv"


# Excel extracted settings
excel_headers = [
    "Item Number",
    "number",
    "Quantity",
    "Equipment",
    "Module",
    "Level of significance",
    "Category",
    "Other Information",
    "UOM",
    "ST",
    "Description 1",
    "Description 2",
    "Search Text",
    "Unit Cost",
    "Extended Cost",
    "jdelitm",
    "prp1",
    "prp2",
    "file_name",
    "Type",
    "DIM",
    "Comm Class",
    "Supplier",
    "Item Pool",
    "Drawing2",
]


# equivalent ->  Excel position & columns name of the data
# e.g. the data in excel column 'A2' is from  spl.part_number
#   column: spl(dataframe)  #Title in Spl
dict_header = {
    "A2": "part_number",  # "Item Number"
    "B2": "number",  # "Number(Drawing)"
    "C2": "quantity",  # "Quantity"
    "E2": "module",  # "Module",
    "F2": "possibility",  # "Level of significance"
    "I2": "unit_of_measure",  # "UOM"
    "J2": "stocking_type",  # "ST"
    "K2": "description_1",  # "Description 1"
    "L2": "description_2",  # "Description 2"
    "M2": "search_text",  # "Search Text"
    "N2": "unit_cost",  # "UOM"
    "P2": "jdelitm",  # "jdelitm",
    "Q2": "description_prp1",  # "prp1",
    "R2": "description_prp2",  # "prp2",
    "S2": "file_name",  # "file_name"
    "T2": "type",  # "Type",
    "U2": "dim",  # "DIM"
    "V2": "comm_class",  # "Comm Class"
    "W2": "item_pool",  # "Item Pool"
    "X2": "supplier",  # "Supplier"
}


# Headers colors of the cells in Excel.
headers_bg_hue = {"A1:H1": (235, 247, 133), "I1:Z1": (183, 185, 188)}  # yellow  # grey


# Parts you find in a gripper that does not need to be in the spl.
# Only the main assembly is kept in the Spl.
contents_of_gripper = [
    "PT1124830",
    "PT0078604",
    "PT0078603",
    "24104091",
    "24101598",
    "24101597",
    "171257",
    "171259",
    "171256",
    "171255",
    "24100056",
    "PT0078602",
    "PT0078601",
    "EEG58C7007P-1",
    "24100360",
    "EEG58C6002P-6",
    "54010220",
    "24300030",
    "24104854",
    "24104591",
    "24104548",
    "122896",
    "122857",
    "162925_EEG58C",
    "171228",
]
# "162922", #(remove ALBP: 2019-09-16)


# File names
output_1 = "template(0).xlsx"
output_2 = "template(1).xlsx"
output_3 = "SPL.xlsx"

# Colors:
orange = (255, 145, 36)  # electric
mauve = (157, 46, 255)  # mauve  Item O ou U
blue = (52, 106, 232)  # blue  -   Item tjrs à revalider
