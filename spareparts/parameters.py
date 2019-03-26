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
        "Type",
        "drawing"
]

#equivalent ->  Excel position & columns name of the data
#e.g. the data in excel column 'A2' is from  spl.part_number
dict_header = {
    'A2':'part_number', #"Item Number"
    'B2':'drawing_number', #"Drawing"
    'C2':'quantity', #"Quantity"
    'E2':'module',
    'F2':'possibility',#"Level of significance"
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
    'T2':'type',
    'U2':'drawing'
}

#color cells
color_bg = {
    # 'I:M' : (235, 247, 133), #yellow
    'A1:C1': (170, 203, 255), #blue
    'D1:H1': (183, 185, 188), #grey
    'I1:M1': (122, 216, 117), #green
    'N1:R1': (122, 100, 100) #red
}


#parts you find in a gripper that does not need to be in the spl
contents_of_gripper = ["PT1124830",
                        "PT0078604",
                        "PT0078603",
                        "24104091",
                        "24101598",
                        "24101597",
                        "171257",
                        "171259",
                        "171256",
                        "24100056",
                        "171255",
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
                        "162922",
                        "122896",
                        "122857",
                        "162925_EEG58C"]

categories = {
'plates' : {
    'prp1': ['Aluminium','Stainless Steel','Steel'],
    'prp2':[]
    }
,
'boulonnerie' : {
    'prp1': ['Inch Fastener','Inch Hardware','Metric Fastener','Metric Hardware'],
    'prp2':[]
    }
,
'bin' : {
    'prp1': ['Sign & Label','Synthetic Product','Plumbing Hardware','Pièce Manufacturée Magasin'],
    'prp2': []
    }
,
'items_electric' : {
    'prp1':['Electric Component'],
    'prp2':[]
    }
}
