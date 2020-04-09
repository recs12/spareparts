#!python3
# -*- coding: utf-8 -*-

from logzero import logger

import click
from spareparts.compare import differences
from spareparts.db import generate_levels_report
from spareparts.lib.grinder import Spareparts
from spareparts.lib.info import headlines
from spareparts.lib.settings import ACRONYM, splname, template1, template2


@click.group()
def cli():
    pass

@cli.command(help="- Compare two spareparts.")
@click.argument("spl1", nargs=1)
@click.argument("spl2", nargs=1)
def compare(spl1, spl2):
    differences(spl1, spl2)

@cli.command("version")
def version():
    print("Spareparts 1.1.2")

@cli.command("create", help="- Generate spareparts list in an excel format.")
def main():
    try:
        logger.info(headlines)
        machine = Spareparts()
        machine.prompt_confirmation()
        machine.generate_spl()
        machine.load_db()
        machine.part_type()
        machine.equivalences()
        machine.drawing_number()
        machine.strain()
        machine.lines_numbers()
        machine.create_excel(template1)
        machine.edit_excel(template1, template2)
        machine.colors_excel(template2, splname)
        machine.del_templates()
        print("Process completed successfully.")
    except FileNotFoundError as err:
        logger.error(f"[!][{err}]")
    except FileExistsError as err:
        logger.error(f"[!][{err}]")
    else:
        pass
    finally:
        pass


@cli.command(help=f"- Generate <level.csv> to store in T:\TEMPO\{ACRONYM}")
def levels():
    generate_levels_report()


if __name__ == "__main__":
    cli()

# TODO: [1] empty folder handling
# TODO: [1] write docs > pycco (print paper format tabloid)
# TODO: [3] correction - close excel file at end of process
# TODO: [3] write test:: strain by modifiying the class Spareparts
