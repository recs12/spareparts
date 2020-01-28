#!python3

import pytest
import pandas as pd
from spareparts.lib.grinder import Spareparts

class Tweaked(Spareparts):
    
    def __init__(self):
        self.spl = pd.read_csv(r'./samples/nuts.csv')
        self.spl_empty = pd.DataFrame()
        self.db = pd.DataFrame()
        self.asm = pd.DataFrame()
        self.elec = pd.DataFrame()
        self.garbage = pd.DataFrame()
        self.nuts = pd.DataFrame()
        self.plates = pd.DataFrame()
        self.gearbox = pd.DataFrame()
        self.drawings = {}


machine = Tweaked()

def _nuts():
    result = machine.strain()
    #assert(result.spl == expected)

# @pytest.fixture
# def nuts(x):
#     fastener = Spareparts()
#     return x + 1

# def test_answer():
#     assert func(3) == 4



#TODO: tweek the Spareparts class to test xlsx sample file filter.