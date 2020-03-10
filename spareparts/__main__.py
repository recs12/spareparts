#!python3
# -*- coding: utf-8 -*-

from loguru import logger
import functools
from glob import glob
import os, sys
import numpy as np
import pandas as pd
import xlwings as xw
from spareparts.lib.grinder import Colors
from spareparts.lib.grinder import Spareparts
from spareparts.lib.settings import output_1, output_2, output_3
import click

from .db import generate_levels_report
from .compare import differences

@click.group()
def cli():
    pass

@cli.command()
@click.argument("spl1", nargs=1)
@click.argument("spl2", nargs=1)
def compare(spl1, spl2):
    differences(spl1, spl2)

@cli.command()
def levels():
    generate_levels_report()

@cli.command()
def create():
    try:
        machine = Spareparts()
        machine.prompt_confirmation()
        machine.generate_spl()
        machine.load_db()
        machine.part_type()
        machine.equivalences()
        machine.drawing_number()
        machine.strain()
        machine.lines_numbers()
        machine.create_excel(output_1)
        machine.edit_excel(output_1, output_2)
        machine.colors_excel(output_2, output_3)
        machine.del_templates()
    except FileNotFoundError as err:
        print(f"[!][{err}]")
    except FileExistsError as err:
        print(f"[!][{err}]")
    else:
        pass
    finally:
        pass


if __name__ == '__main__':
    cli()

# TODO: [1] empty folder handling
# TODO: [1] write docs > pycco (print paper format tabloid)
# TODO: [3] correction - close excel file at end of process
# TODO: [3] write test:: strain by modifiying the class Spareparts
        #  e.g. test_Spareparts(Spareparts) = __init__: super().spl = pd.Dataframe()  empty it
        # then reinjecte sample of new data
# TODO: [3] move loop to generator
