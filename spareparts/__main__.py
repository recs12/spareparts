#!python3
# -*- coding: utf-8 -*-

import logzero
from logzero import logger

import click
from spareparts.compare import differences
from spareparts.db import generate_levels_report
from spareparts.lib.grinder import Colors, Spareparts
from spareparts.lib.settings import ACRONYM, output_1, output_2, output_3
from spareparts.lib.info import headlines

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
        print(headlines)
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
        logger.info("Process completed successfully.")
    except FileNotFoundError as err:
        logger.info(f"[!][{err}]")
    except FileExistsError as err:
        logger.info(f"[!][{err}]")
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

