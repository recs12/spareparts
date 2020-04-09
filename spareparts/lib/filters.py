import pandas as pd
from spareparts.lib.decorators import special_pt, special_desc_2, special_desc_1


def adjust_significance_notnull(spl, garbage):
    """relocate the significance is not nan"""
    relocate = garbage[garbage.possibility.notna()]
    garbage = garbage[~garbage.possibility.notna()]
    spl = pd.concat([spl, relocate], ignore_index=True)
    return (spl, garbage, relocate)


def trash_parts_ending_P1_or_A1(spl, garbage):
    """filter --> number_P1.par  & number_A1.par"""
    relocate = spl[spl["part_number"].str.contains(r"\d{6}_[P|A]?\d{1}").values]
    spl = spl[~spl["part_number"].str.contains(r"\d{6}[_|-][P|A]?\d{1}").values]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


@special_pt("PT1111808")
@special_pt("PT0038724")
@special_pt("EEG58C6000A-.*")
def trash_assemblies(spl, garbage):
    """filter -> ASSEMBLY (with exceptions)"""
    relocate = spl[(spl.unit_of_measure.isna()) & (spl.type == "asm")]
    spl = spl[~((spl.unit_of_measure.isna()) & (spl.type == "asm"))]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


def trash_robot(spl, garbage):
    """robot -> garbage"""
    relocate = spl[spl.type.isin(["LR Mate"])]
    spl = spl[~spl.type.isin(["LR Mate"])]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


@special_pt("122857")
@special_pt("122896")
@special_pt("214938")
@special_pt("24300030")
@special_pt("162045")
def trash_description(spl, garbage, keyword, description="description_1"):
    """description_1 OR description_2"""
    relocate = spl[spl[description].str.contains(keyword, na=False, regex=True)]
    spl = spl[~spl[description].str.contains(keyword, na=False, regex=True)]
    garbage = pd.concat([garbage, relocate], ignore_index=True, sort=False)
    return (spl, garbage, relocate)


@special_desc_1(r"O-RING-NITRILE")
@special_pt("157930")
def trash_fastener(spl, garbage, prp1=[50, "50", 90, "90"]):
    """Filter for fastener"""
    relocate = spl[spl.comm_class.isin(prp1)]
    spl = spl[~spl.comm_class.isin(prp1)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


def trash_prp(spl, garbage, prp1, prp2):
    """prp1, prp2"""
    relocate = spl[spl.description_prp1.isin(prp1) & spl.description_prp2.isin(prp2)]
    spl = spl[~(spl.description_prp1.isin(prp1) & spl.description_prp2.isin(prp2))]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


@special_pt("PT0032489")
@special_desc_2(r"Retaining Ring")
@special_desc_2(r"Seal")
@special_desc_2(r"Door&Panel, Hardware&Furniture")
@special_desc_2(r"Coupling, Bushing & Shaft Acc.")
@special_desc_2(r"Door&Panel, Hardware&Furniture")
@special_desc_2(r"Spring, Shock & Bumper")
@special_desc_2(
    r".*?\bBARB\b.*?\bNYLON\b.*?"
)  # regex: line with both words BARB and bNYLON.
@special_desc_1("BFR")
@special_desc_1("BUMPER")
def trash_prp1(spl, garbage, prp1):
    """prp1"""
    relocate = spl[spl.description_prp1.isin(prp1)]
    spl = spl[~spl.description_prp1.isin(prp1)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


@special_pt("PT0015199")
@special_pt("PT1003110")
@special_pt("PT1072543")
@special_pt("PT1101791")
@special_pt("PT1114199")
@special_pt("PT1115438")
@special_pt("PT1123123")
@special_pt("PT1131265")
def trash_item_number(spl, garbage, list_parts):
    """filter -> parts inside the gripper"""
    relocate = spl[spl.part_number.isin(list_parts)]
    spl = spl[~spl.part_number.isin(list_parts)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


def trash_file_name(spl, garbage, keyword):
    """filter -> par in /file_name/"""
    relocate = spl[spl.file_name.str.contains(keyword, na=False, regex=True)]
    spl = spl[~spl.file_name.str.contains(keyword, na=False, regex=True)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)
