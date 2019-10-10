#!python3
# -*- coding: utf-8 -*-
"""
1. **Generate spl**
python -m spareparts

2. **Generate level data**
python -m spareparts.db

3. **Compare two spareparts lists**
python -m spareparts.compare

"""

from loguru import logger
import functools
from glob import glob
import os, sys
import bashplotlib
import numpy as np
import pandas as pd
import xlwings as xw
from spareparts.lib.grinder import Colors
from spareparts.lib.grinder import Spareparts
from spareparts.lib.settings import output_1, output_2, output_3


def main(model='levels.csv'):
    """manipulation of the date before creating the excel file"""
    machine = Spareparts(model)
    machine.prompt_confirmation()
    machine.generate_spl()
    machine.load_db(model)
    machine.part_type()
    machine.equivalences()
    machine.drawing_number()
    machine.strain()
    machine.lines_numbers()
    machine.create_excel(output_1)
    machine.edit_excel(output_1, output_2)
    machine.colors_excel(output_2, output_3)
    machine.del_templates()

if __name__ == "__main__":
    main()

#TODO: [1] name change:: all.csv - > levels.csv
#TODO: [1] add all the tabs in excel related to spl for end-users
#TODO: [1] setup path to  levels.csv in each user tempo.
#TODO: [1] move gripper into strain file instead of settings.py
#TODO: [1] write docs > pycco (print paper format tabloid)
#TODO: [1] for db command- insert date in name file. like levels_2019_09_01.csv
#TODO: [2] make an .exe (icon available in GitHub)
#TODO: [2] exception.pt_num() like organization
#TODO: [3] deactivate loguru
#TODO: [3] implement bashplotlib
#TODO: [3] refactore:: strain
#TODO: [3] change module to levels.csv
#TODO: [3] correction - close excel file at end of process
#TODO: [3] group command with click spl(optional) - levels - compare with arg1 arg2)
#TODO: [3] write test:: strain by modifiying the class Spareparts
#  e.g. test_Spareparts(Spareparts) = __init__: super().spl = pd.Dataframe()  empty it
# then reinjecte sample of new data 
#TODO: [3] wrong format of txt file handling
#TODO: [3] empty folder handling
