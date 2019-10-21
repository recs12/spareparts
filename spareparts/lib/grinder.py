import sys
import functools
import bashplotlib
import numpy as np
import pandas as pd
import xlwings as xw
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from loguru import logger
from spareparts.lib.settings import *


def special_pt(regx):
    """decorator"""

    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[
                assem.part_number.str.contains(regx, na=False, regex=True)
            ]
            assem = assem[~assem.part_number.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)

        return _wrapper

    return _outer_wrapper


def special_desc_1(regx):
    """decorator"""

    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[
                assem.description_1.str.contains(regx, na=False, regex=True)
            ]
            assem = assem[~assem.description_1.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)

        return _wrapper

    return _outer_wrapper


def special_desc_2(regx):
    """decorator"""

    def _outer_wrapper(wrapped_function):
        @functools.wraps(wrapped_function)
        def _wrapper(*args, **kwargs):
            spl, garbage, assem = wrapped_function(*args, **kwargs)
            item_keep = assem[
                assem.description_2.str.contains(regx, na=False, regex=True)
            ]
            assem = assem[~assem.description_2.str.contains(regx, na=False, regex=True)]
            spl = pd.concat([spl, item_keep], ignore_index=True, sort=False)
            return (spl, garbage, assem)

        return _wrapper

    return _outer_wrapper


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


def trash_robot(spl, garbage, criteres=["LR Mate"]):
    """robot -> garbage"""
    relocate = spl[spl.type.isin(criteres)]
    spl = spl[~spl.type.isin(criteres)]
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
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


@special_desc_1(r"O-RING-NITRILE")
@special_pt("157930")
def trash_fastener(spl, garbage, prp1=["50", "90"]):
    """Filter for fastener"""
    relocate = spl[spl.comm_class.isin(prp1)]
    spl = spl[~spl.comm_class.isin(prp1)]
    garbage = pd.concat([garbage, relocate], ignore_index=True)
    return (spl, garbage, relocate)


def trash_prp(spl, garbage, prp1=[], prp2=[]):
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
def trash_prp1(spl, garbage, prp1=[]):
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


class Colors(object):
    def electric(prp1, color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.prp1.isin(prp1)].tolist()
                for row in targeted_index:
                    cellule = (
                        f"A{row+2}:U{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    def obsolete(color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.ST.isin(["O", "U"])].tolist()
                for row in targeted_index:
                    cellule = (
                        f"J{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    def meter_foot(color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.UOM.isin(["MT", "FT", "RL", "SF"])].tolist()
                for row in targeted_index:
                    cellule = (
                        f"I{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    electric = staticmethod(electric)
    obsolete = staticmethod(obsolete)
    meter_foot = staticmethod(meter_foot)


class Spareparts(object):
    """Generate spareparts list."""

    JDEPATH = (
        r"Z:\Pour membres de MHPS\SUIVI DE LA FABRICATION\Item PTP JDE\INV-PTP-JDE.xlsx"
    )
    JDE_TEMP = os.path.join(tempo_local, temp_jde)

    def __init__(self, model):
        self.model = model
        self.jde = self.load_jde_data()
        self.db = pd.DataFrame()

        self.spl = pd.DataFrame()
        self.asm = pd.DataFrame()
        self.elec = pd.DataFrame()
        self.garbage = pd.DataFrame()
        self.nuts = pd.DataFrame()
        self.plates = pd.DataFrame()
        self.drawings = {}

    @staticmethod
    def prompt_confirmation():
        "ask user to resume the program"
        print(f"Run: {__file__}")
        answer = input("Proceed ([y]/n) ?:  ")
        if answer.lower() in ["yes", "y"]:
            pass
        else:
            print("Process has stopped.")
            sys.exit()

    def generate_spl(self):
        files = (file for file in Spareparts.listing_txt_files())
        parts = pd.concat(
            [Spareparts.extract_data(file) for file in files], ignore_index=True
        )
        self.spl = Spareparts.joining_spl_jde(self.jde, parts)
        self.spl.part_number = (
            self.spl.part_number.str.strip()
        )  # strip part_number column

    def load_db(self, model):
        """load the item-level database"""
        db_model = os.path.join(tempo_local, model)
        if not os.path.exists(db_model):
            self.db = pd.DataFrame()
        else:
            df = pd.read_csv(db_model, dtype={"possibility": str})
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            df.item_number = df.item_number.astype(str)
            df.item_number = df.item_number.str.strip()
            df.possibility = df.possibility.astype(str)
            df.possibility = df.possibility.str.strip()
            self.db = df[["item_number", "possibility"]]
        self.spl = self.spl.join(self.db.set_index("item_number"), on="jdelitm")

    @staticmethod
    def loading_spl(path):
        """load the data from spl list"""
        if not os.path.exists(path):
            raise FileNotFoundError("Check if spl path is correct.")
        else:
            spl = pd.read_excel(path, sheet_name="Sheet1")
            spl.columns = spl.columns.str.strip().str.lower().str.replace(" ", "_")
            spl.item_number = spl.item_number.astype("str")
            spl = spl[["item_number"]]
            return spl

    @staticmethod
    def load_jde_data():
        """"""
        JDE_TEMP = Spareparts.JDE_TEMP
        if os.path.exists(JDE_TEMP):
            answer = input(
                f"Do you want to load the temporary jde? (fast) \n Path:{JDE_TEMP}\n Proceed ([y]/n) ?:"
            )
            if answer.lower() in ["yes", "y"]:
                jde_temp = pd.read_csv(JDE_TEMP)
                return jde_temp
            else:
                print("Process interrupted.")
                sys.exit()
        else:
            jde_data = Spareparts.extract_jde()
            jde_data.to_csv(JDE_TEMP, index=False)
            return jde_data

    @staticmethod
    def extract_jde():
        """"""
        # add a try - except (in case the file is not found)
        print(f"Path: PTP-JDE: {Spareparts.JDEPATH}\n-> Loading the JDE Inventory...")
        df = pd.read_excel(
            Spareparts.JDEPATH,
            sheet_name=0,
            skiprows=[0, 1, 2, 3],
            usecols="A,C,P,E,H,I,K,O,U,X,AA,AR,AT,CB",
            dtype={"Business Unit": int, "Unit Cost": float},
        )
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df = df[df.business_unit == 101]
        return df

    @staticmethod
    def extract_data(fichier):
        """"""
        # add try and except
        df = pd.read_csv(
            fichier,
            delimiter="\t",
            skiprows=[0, 2],
            header=1,
            names=[
                "Part Number",
                "Revision",
                "DSC_A",
                "JDELITM",
                "DIM",
                "Quantity",
                "File Name",
            ],
            index_col=False,
            encoding="latin3",
            error_bad_lines=False,
            na_values="-",
        )
        # clean the columns
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        df["jdelitm"] = df["jdelitm"].str.strip()
        df = Spareparts.replacing_C01(df)
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerse")
        df = df.groupby(
            ["part_number", "revision", "dsc_a", "dim", "jdelitm", "file_name"],
            as_index=False,
        )["quantity"].sum()
        df = df.replace(r"^-?\s+$", np.nan, regex=True)
        df = df.dropna(subset=["part_number", "jdelitm"])
        # give the module number
        module_number = os.path.splitext(os.path.basename(fichier))[0]
        df["module"] = module_number
        print(f" [+][\t{module_number}\t]")
        return df

    @staticmethod
    def listing_txt_files():
        """"""
        for file in os.listdir(r"."):
            if file.endswith(".txt"):
                yield file

    @staticmethod
    def replacing_C01(df):
        """Replacing 123456_C01 to 123456."""
        pat = r"(?P<number>\d{6})(?P<suffixe>_C\d{2})"
        repl = lambda m: m.group("number")
        df["part_number"] = df["part_number"].str.replace(pat, repl)
        return df

    @staticmethod
    def joining_spl_jde(jde, parts):
        """transform the jde column to string format
        join the parts documents with the jde on jdelitm column
        and sort it on column:module
        """
        jde.item_number = jde.item_number.astype(str)
        spl = parts.join(jde.set_index("item_number"), on="jdelitm").sort_values(
            "module"
        )
        return spl

    def part_type(self):
        """create a column type --> .par .psm .asm"""
        self.spl["type"] = self.spl.file_name.str.split(".").str[-1].str.strip()
        self.spl.type = self.spl.type.str.lower()

    def lines_numbers(self):
        print(
            "\n"
            "-------------------------\n"
            f"spl       :\t{self.spl.shape[0]}\n"
            f"garbage   :\t{self.garbage.shape[0]}\n"
            f"plates    :\t{self.plates.shape[0]}\n"
            f"elec      :\t{self.elec.shape[0]}\n"
            f"asm       :\t{self.asm.shape[0]}\n"
            f"nuts      :\t{self.nuts.shape[0]}\n"
            "-------------------------\n"
        )
        # TODO: Bashplotlib
        # from bashplotlib.horizontal_histogram import plot_horiz_hist

        # plot_horiz_hist(
        #     'scratch_data.txt',
        #     title='Horizontal Histogram!',
        #     ylab=True,
        #     show_summary=True)

    def create_excel(self, given_name_xlsx):
        """fill the tabs in excel file with the dataframes"""
        tabs = {
            "nuts": self.nuts,
            "asm": self.asm,
            "plates": self.plates,
            "elec": self.elec,
            "garbage": self.garbage,
            "spl": self.spl,
        }
        wb = xw.Book()  # this will create a new workbook
        for tab in tabs.keys():
            sht = wb.sheets.add(tab)
        for tab, df in tabs.items():
            sht = wb.sheets[
                tab
            ]  # skip the Sheet1 and create spl within a loop for all tab
            sht.range("A1").value = excel_headers  # insert headers (horizontal)
            sht.range("A1:R1").api.Font.Bold = True  # bold headers (horizontal)
            for rang, color in headers_bg_hue.items():
                xw.Range(rang).color = color
            for colum, data in dict_header.items():
                sht.range(colum).options(index=False, header=False).value = df[data]
            sht.autofit()
        wb.sheets["Sheet1"].delete()
        wb.save(given_name_xlsx)
        wb.close()

    @staticmethod
    def edit_excel(file_name, new_name):
        wb = load_workbook(file_name)
        for s in wb.sheetnames:
            ws = wb[s]
            MAX_ = ws.max_row
            field = f"A1:X{MAX_}"
            ws.auto_filter.ref = field
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            significance_column = ws["F"]
            for cell in significance_column:
                cell.alignment = Alignment(horizontal="center")
        wb.save(new_name)
        wb.close()

    def refine(self):
        ambiguous = self.spl[
            ~(
                (self.spl.possibility == "1")
                | (self.spl.possibility == "2")
                | (self.spl.possibility == "3")
            )
        ]
        ambiguous_items = (
            ambiguous.part_number.str.strip().tolist()
        )  # Whitespaces stripped here
        for itm in ambiguous_items:
            mdl = self.spl.loc[itm, "module"]  # module => mdl
            self.spl.possibility[
                self.spl.part_number == itm, "possibility"
            ] = self.db.loc[itm, mdl]

    @Colors.obsolete(mauve)
    @Colors.meter_foot(blue)
    @Colors.electric(["Electric Component"], orange)
    def extraction(file_name, workbook, sht_name):
        df = pd.read_excel(file_name, sheet_name=sht_name)
        sht = workbook.sheets[sht_name]
        return (df, sht)

    extraction = staticmethod(extraction)

    @staticmethod
    def add_colors(selected_file, sheet_spl):
        wb = xw.Book(selected_file)
        Spareparts.extraction(selected_file, wb, sheet_spl)
        return wb

    def colors_excel(self, selected_file, new_file):
        args = {
            "nuts": self.nuts,
            "asm": self.asm,
            "plates": self.plates,
            "elec": self.elec,
            "garbage": self.garbage,
            "spl": self.spl,
        }
        for tab in args:
            wb = Spareparts.add_colors(selected_file, tab)
        wb.save(new_file)
        wb.close()

    @staticmethod
    def log_report(_df, df_name):
        from loguru import logger

        _df["groupe"] = df_name
        logger.info(
            "\ndf_name:\n" + _df[["groupe", "part_number", "description_1"]].to_string()
        )

    def strain(self):
        """Filters of unwanted parts here."""

        logger.add("report_{time}.log", level="INFO")


        #--------------------------------------------------------------------#
        #                                                                    #
        #                           START FILTERS HERE                       #
        #                                                                    #
        #--------------------------------------------------------------------#


        # === plates ===
        plates_prp1 = ["Aluminium", "Stainless Steel", "Steel"]
        self.spl, self.garbage, _plates = trash_prp1(
            self.spl, self.garbage, prp1=plates_prp1
        )
        self.garbage = pd.concat([self.garbage, _plates]).drop_duplicates(keep=False)
        Spareparts.log_report(_plates, "_plates")

        # === fasteners ===
        self.spl, self.garbage, _nuts = trash_fastener(self.spl, self.garbage)
        self.garbage = pd.concat([self.garbage, _nuts]).drop_duplicates(keep=False)
        Spareparts.log_report(_nuts, "_nuts")

        # === assemblies ===
        self.spl, self.garbage, _asm = trash_assemblies(
            self.spl, self.garbage
        )  # _ASM SEEMS TO BE THE EXCEPTION
        self.garbage = pd.concat([self.garbage, _asm]).drop_duplicates(keep=False)
        Spareparts.log_report(_asm, "_asm")

        # === uncategorized ===
        self.garbage_prp1 = [
            "Sign & Label",
            "Plumbing Hardware",
            "Pièce Manufacturée Magasin",
        ]
        self.spl, self.garbage, _uncatego = trash_prp1(
            self.spl, self.garbage, prp1=self.garbage_prp1
        )
        self.garbage = pd.concat([self.garbage, _uncatego]).drop_duplicates(keep=False)
        Spareparts.log_report(_uncatego, "_uncatego")

        # === robot ===
        self.spl, self.garbage, _robot = trash_robot(self.spl, self.garbage)
        self.garbage = pd.concat([self.garbage, _robot]).drop_duplicates(keep=False)
        Spareparts.log_report(_robot, "_robot")

        # === gripper ===
        self.spl, self.garbage, _inside_gripper = trash_item_number(
            self.spl,
            self.garbage,
            list_parts=contents_of_gripper,  # The contents of gripper in the file settings.
        )
        self.garbage = pd.concat([self.garbage, _inside_gripper]).drop_duplicates(
            keep=False
        )
        Spareparts.log_report(_inside_gripper, "_inside_gripper")

        # === industrial ===
        self.spl, self.garbage, _industrial = trash_prp(
            self.spl, self.garbage, prp1=["Industrial Engine"], prp2=["Engine Parts"]
        )
        self.garbage = pd.concat([self.garbage, _industrial]).drop_duplicates(
            keep=False
        )
        Spareparts.log_report(_industrial, "_industrial")

        # === _furniture ===
        self.spl, self.garbage, _furniture = trash_prp(
            self.spl, self.garbage, prp1=["Factory Furniture"], prp2=["Tape"]
        )
        self.garbage = pd.concat([self.garbage, _furniture]).drop_duplicates(keep=False)
        Spareparts.log_report(_furniture, "_furniture")

        # === _gearbox ===
        self.spl, self.garbage, _gearbox = trash_prp(
            self.spl,
            self.garbage,
            prp1=["Mechanical Component"],
            prp2=["Gearbox, Gear, Rack & Pinion", "Gear Motor & Motor"],
        )
        self.garbage = pd.concat([self.garbage, _gearbox]).drop_duplicates(keep=False)
        Spareparts.log_report(_gearbox, "_gearbox")

        # === _sheave ===
        """ALBP(2019-09-16): TIMING BELT SHEAVE kept in SPL."""

        # === _grommet ===
        self.spl, self.garbage, _grommet = trash_description(
            self.spl, self.garbage, keyword="GROMMET;RUBBER"
        )
        self.garbage = pd.concat([self.garbage, _grommet]).drop_duplicates(keep=False)
        Spareparts.log_report(_grommet, "_grommet")

        # === _manif ===
        self.spl, self.garbage, _manif = trash_description(
            self.spl,
            self.garbage,
            keyword=r"PNEU.VALVE\sMANIFOLD\s[\d/\d\:\d{2}|\d\:\d{2}]",
            description="description_1",
        )
        self.garbage = pd.concat([self.garbage, _manif]).drop_duplicates(keep=False)
        Spareparts.log_report(_manif, "_manif")

        # === _pneu_frl ===
        self.spl, self.garbage, _pneu_frl = trash_description(
            self.spl,
            self.garbage,
            keyword=r"PNEU\.F\.R\.L",
            description="description_1",
        )
        self.garbage = pd.concat([self.garbage, _pneu_frl]).drop_duplicates(keep=False)
        Spareparts.log_report(_pneu_frl, "_pneu_frl")

        # === _clamp ===
        self.spl, self.garbage, _clamp = trash_description(
            self.spl,
            self.garbage,
            keyword="CLAMP;TRANSPORT UNIT",
            description="description_2",
        )
        self.garbage = pd.concat([self.garbage, _clamp]).drop_duplicates(keep=False)
        Spareparts.log_report(_clamp, "_clamp")

        # === electric ===
        self.spl, self.garbage, _elec = trash_prp(
            self.spl,
            self.garbage,
            prp1=["Electric Component"],
            prp2=[
                "Cable Tray & Cable Carrier",
                "Conduits & fittings",
                "Enclosures",
                "Sensors",
                "Lights & bulbs",
                "Switches",
                "General hardware",
                "Stickers",
                "Buttons & pilot lights",
                "Connectors & crimps",
            ],
        )
        self.garbage = pd.concat([self.garbage, _elec]).drop_duplicates(keep=False)
        print(f"***_elec: {_elec}")

        Spareparts.log_report(_elec, "_elec")

        # === _par ===
        self.spl, self.garbage, _par = trash_file_name(
            self.spl, self.garbage, keyword=r"^par\s*$"
        )
        self.garbage = pd.concat([self.garbage, _par]).drop_duplicates(keep=False)
        Spareparts.log_report(_par, "_par")

        # === _P1_A1 ===
        self.spl, self.garbage, _P1_A1 = trash_parts_ending_P1_or_A1(
            self.spl, self.garbage
        )
        self.garbage = pd.concat([self.garbage, _P1_A1]).drop_duplicates(keep=False)
        Spareparts.log_report(_P1_A1, "_P1_A1")

        # === _housed_cap ===
        """ALBP(2019-09-16): House-brg-cap kept in SPL."""

        # === _collar ===
        collar = r"COLLAR"
        self.spl, self.garbage, _collar = trash_description(
            self.spl, self.garbage, keyword=collar
        )
        self.garbage = pd.concat([self.garbage, _collar]).drop_duplicates(keep=False)
        Spareparts.log_report(_collar, "_collar")

        # === fpmr ===
        fpmr = r"FIXING PLATE MOTOR ROLLER"
        self.spl, self.garbage, _fpmr = trash_description(
            self.spl, self.garbage, keyword=fpmr
        )
        self.garbage = pd.concat([self.garbage, _fpmr]).drop_duplicates(keep=False)
        Spareparts.log_report(_fpmr, "_fpmr")

        # === _fit ===
        fit = r"PNEU.FIT.NIPPLE"
        self.spl, self.garbage, _fit = trash_description(
            self.spl, self.garbage, keyword=fit
        )
        self.garbage = pd.concat([self.garbage, _fit]).drop_duplicates(keep=False)
        Spareparts.log_report(_fit, "_fit")

        # === miscellaneous ===
        rejected_parts = [
            "DPP95A1530S-3",
            "136918",
            "216081",
            "162463",
            "146660",
            "02479",
            "EEG59F2164P-9151967",
        ]
        self.spl, self.garbage, _misc = trash_item_number(
            self.spl, self.garbage, rejected_parts
        )
        self.garbage = pd.concat([self.garbage, _misc]).drop_duplicates(keep=False)
        Spareparts.log_report(_misc, "_misc")

        # === _keysquare ===
        self.spl, self.garbage, _keysquare = trash_description(
            self.spl, self.garbage, keyword="KEY;SQUARE"
        )
        self.garbage = pd.concat([self.garbage, _keysquare]).drop_duplicates(
            keep=False
        )
        Spareparts.log_report(_keysquare, "_keysquare")

        # === _stud ===
        self.spl, self.garbage, _stud = trash_description(
            self.spl, self.garbage, keyword="STUD"
        )
        self.garbage = pd.concat([self.garbage, _stud]).drop_duplicates(keep=False)
        Spareparts.log_report(_stud, "_stud")

        # === _suppliers ===
        self.spl, self.garbage, _suppliers = trash_description(
            self.spl, self.garbage, keyword="SOUS-TRAITANCE RECOUVREMENT"
        )
        self.garbage = pd.concat([self.garbage, _suppliers]).drop_duplicates(keep=False)
        Spareparts.log_report(_suppliers, "_suppliers")

        # === weldnut ===
        self.spl, self.garbage, _weldnut = trash_description(
            self.spl, self.garbage, keyword="WELD NUT"
        )
        self.garbage = pd.concat([self.garbage, _weldnut]).drop_duplicates(keep=False)
        Spareparts.log_report(_weldnut, "_weldnut")

        # === _transparent ===
        self.spl, self.garbage, _transparent = trash_prp(
            self.spl, self.garbage, prp1=["POLYCARBONATE PLATE"], prp2=["TRANSPARENT"]
        )
        self.garbage = pd.concat([self.garbage, _transparent]).drop_duplicates(
            keep=False
        )
        Spareparts.log_report(_transparent, "_transparent")

        # === _hoffman_pkg ===
        self.spl, self.garbage, _hoffman_pkg = trash_item_number(
            self.spl, self.garbage, list_parts=["PT1173377", "PT1173378"]
        )
        self.garbage = pd.concat([self.garbage, _hoffman_pkg]).drop_duplicates(
            keep=False
        )
        Spareparts.log_report(_hoffman_pkg, "_hoffman_pkg")

        #--------------------------------------------------------------------#
        #                           END FILTERS HERE                         #
        #--------------------------------------------------------------------#

        self.spl = self.spl.drop_duplicates(keep=False)
        # Garbage include all filtered parts
        self.garbage =  pd.concat([self.garbage,
                                    _uncatego,
                                    _inside_gripper,
                                    _industrial,
                                    _furniture,
                                    _grommet,
                                    _manif,
                                    _pneu_frl,
                                    _clamp,
                                    _par,
                                    _collar,
                                    _fpmr,
                                    _fit,
                                    _misc,
                                    _stud,
                                    _keysquare,
                                    _stud,
                                    _suppliers,
                                    _weldnut,
                                    _transparent,
                                    _hoffman_pkg,
                                    ], ignore_index=True, sort=False).drop_duplicates(keep=False)
        self.asm = _asm
        self.elec = _elec
        self.nuts = _nuts
        self.plates = _plates


    def equivalences(self):
        """return dictionnary > {ptnumber:drawing number}"""
        prt_num = self.spl.part_number
        prt_num = prt_num[
            prt_num.str.contains(
                r"\bPT\d{7}\b|\bEEG.*\b|\bEPT.*\b", na=False, regex=True
            )
        ]  # debug r'PT\d{7}|EEG|EPT'
        prt_num = prt_num.str.strip().tolist()
        # drawing number is found in JDE:'drawing_number'
        _drawing = "drawing_number"
        _item = "item_number"
        itm_num_drawing = self.jde[[_item, _drawing]]
        itm_num_drawing = itm_num_drawing.set_index(_drawing)
        equivalences = {}
        for i in prt_num:
            if i in itm_num_drawing.index.tolist():
                if len(itm_num_drawing.loc[i, _item]) == 6:
                    equivalences[i] = itm_num_drawing.loc[i, _item]
        self.drawings = equivalences

    def drawing_number(self):
        """add column """
        self.spl["number"] = self.spl["part_number"].map(
            self.drawings, na_action="ignore"
        )

    @staticmethod
    def del_templates():
        import os
        os.remove(output_1)
        os.remove(output_2)
