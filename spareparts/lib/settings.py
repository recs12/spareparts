import os
#Link to the JDE on the local network
JDEPATH = r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"
#temporary-files-location (jde_temp, db)
temp_path=os.path.join(os.environ.get('USERPROFILE'),"Spareparts")
#tempo-files-location (jde_temp, db)
tempo_local_drive=os.path.join("T:\tempo\recs","ARCHIVES_SPL")
#name of temporary jde
temp_jde = r'temporary_jde.csv'
#name of database levels
levels_db = r'db.csv'
#Excel extracted settings
excel_headers = [   "Item Number",
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
                    "Drawing",
                    "DIM",
                    "Comm Class",
                    "Item Pool",
]
#equivalent ->  Excel position & columns name of the data
#e.g. the data in excel column 'A2' is from  spl.part_number
#   column: spl(dataframe)  #Title in Spl
dict_header = {
            'A2':'part_number',     #"Item Number"
            'B2':'drawing_number',  #"Drawing"
            'C2':'quantity',        #"Quantity"
            'E2':'module',          #
            'F2':'possibility',     #"Level of significance"
            'I2':'unit_of_measure', #
            'J2':'stocking_type',   #
            'K2':'description_1',   #
            'L2':'description_2',   #
            'M2':'search_text',     #
            'N2':'unit_cost',       #
            'P2':'jdelitm',         #
            'Q2':'description_prp1',#
            'R2':'description_prp2',#
            'S2':'file_name',       #
            'T2':'type',            #
            'U2':'drawing',         #
            'V2':'dim',             #"DIM"
            'W2':'comm_class',      #"Comm Class"
            'X2':'item_pool',       #TODO: "Item Pool" - refer in filter
}
#headers spl color cells
headers_bg_hue = {
                'A1:H1': (235, 247, 133), #yellow
                'I1:X1': (183, 185, 188), #grey
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
                        "162922",
                        "122896",
                        "122857",
                        "162925_EEG58C",
                        "171228"
]

#File names
output_1 = 'auto.xlsx'
output_2 = 'auto_filters.xlsx'
output_3 = 'auto_filters_aligned.xlsx'
