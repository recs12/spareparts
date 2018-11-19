JDEPATH = r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"


#Excel extracted settings
col = ["Item Number",
        "Drawing",
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
        "Type"
]

dict_header = {
    'A2':'part_number',
    'C2':'quantity',
    'E2':'module',
    'I2':'unit_of_measure',
    'J2':'stocking_type',
    'K2':'description_1',
    'L2':'description_2',
    'M2':'search_text',
    'N2':'unit_cost',
    'P2':'jdelitm',
    'Q2':'description_prp1',
    'R2':'description_prp2',
    'S2':'file_name',
    'T2':'type'
}

#color cells
color_bg = {
    # 'I:M' : (235, 247, 133), #yellow
    'A1:C1': (170, 203, 255), #blue
    'D1:H1': (183, 185, 188), #grey
    'I1:M1': (122, 216, 117), #green
    'N1:R1': (122, 100, 100) #red
}