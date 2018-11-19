#!python3

import pandas as pd
from spareparts.categories import categories
import xlwings as xw

# plate1 = categories['plates']
# plate2 = categories['plates']['prp2']
# df = pd.DataFrame(categories)
df = pd.DataFrame(categories['plates'])

wb = xw.Book()  # this will create a new workbook
sht = wb.sheets['Sheet1']

# sht.range('A1').value = df.columns
sht.range('A1').value = df

