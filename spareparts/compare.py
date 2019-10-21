#! python3
# 2019-03-27 by recs
# ===check the current owner of type licenses===

import click
import pandas as pd
import os
from spareparts.lib.settings import tempo_local, temp_jde

# Path to temporary_jde.csv in windows OS.
if os.path.join(tempo_local, temp_jde):
    path_to_jde = os.path.join(tempo_local, temp_jde)
else:
    print("the temporary jde file is not in the TEMPO of RECS")


def extract_items_auto(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name="spl", header=0, usecols="A", dtype={0: str})
    data["Item Number"] = data["Item Number"].str.strip()
    data = data.dropna(how="all")
    serie = pd.Series(data["Item Number"])
    serie = serie.unique().tolist()
    return set(serie)


def extract_items_manual(file):
    """
    Extraction column: item number
    """
    data = pd.read_excel(file, sheet_name="Data", header=0, usecols="A", dtype={0: str})
    data.columns = ["items"]
    data["items"] = data["items"].str.strip()
    data = data.dropna(how="all")
    serie = pd.Series(data["items"])
    serie = serie.unique().tolist()[1:]
    return set(serie)


def parsing_items(spl):
    name_file = str(spl)
    if name_file.startswith("std"):
        return extract_items_manual(name_file)
    elif name_file.startswith("auto"):
        return extract_items_auto(name_file)
    else:
        print(
            f"[Warning] file name: {spl} not reconized, file should start with auto.. or std.."
        )


def joining_spl_jde(jde, parts):
    jde.item_number = jde.item_number.astype(str)
    spl = parts.join(jde.set_index("item_number"), on="item_number")
    return spl


def load_jde_data():
    jde_temp = pd.read_csv(path_to_jde)
    return jde_temp


def delta(spl1, spl2):
    return sorted(list(parsing_items(spl1) - parsing_items(spl2)))


@click.command()
@click.argument("spl1", nargs=1)
@click.argument("spl2", nargs=1)
def main(spl1, spl2):
    click.echo(spl1)
    click.echo(spl2)
    #TODO: Check the name of files to compare.
    df = pd.DataFrame(delta(spl1, spl2), columns=["item_number"])
    jde = load_jde_data()
    parts = joining_spl_jde(jde, df)
    parts.to_csv("difference.csv", index=False)


if __name__ == "__main__":
    main()


# TODO: Can compare pneumatic list option
