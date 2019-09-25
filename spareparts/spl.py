#!python3
# -*- coding: utf-8 -*-

from loguru import logger

import functools
from glob import glob
import os, sys
import bashplotlib
import click
import numpy as np
import pandas as pd
import xlwings as xw
import termgraph
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from spareparts.lib.spare import Colors
from spareparts.lib.spare import Spareparts
from spareparts.lib.settings import *




@click.command()
@click.argument('model')
def generating_spl(model):
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
    generating_spl()
