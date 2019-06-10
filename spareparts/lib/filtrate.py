
from loguru import logger
from spareparts.lib.dispatch import *
from spareparts.lib.settings import *

def log_report(_df, df_name):
    from loguru import logger
    _df['groupe'] = df_name
    logger.info("\ndf_name:\n" + _df[['groupe','part_number','description_1']].to_string())



def strain(spl, garb):

    logger.add("report_{time}.log", level="INFO")

    # === plates ===
    plates_prp1 = ['Aluminium','Stainless Steel','Steel']
    spl, garb, _plates = trash_prp1(spl, garb,
        prp1=plates_prp1,
    )
    garb = pd.concat([garb, _plates]).drop_duplicates(keep=False)
    log_report(_plates, '_plates')


    # === fasteners ===
    boulonnerie_prp1 = ['Inch Fastener','Inch Hardware','Metric Fastener','Metric Hardware']
    spl, garb, _nuts = trash_prp1(spl, garb, prp1=boulonnerie_prp1)
    garb = pd.concat([garb, _nuts]).drop_duplicates(keep=False)
    log_report(_nuts, '_nuts')


    # === assemblies ===
    spl, garb, _asm  = trash_assemblies(spl, garb) #_ASM SEEMS TO BE THE EXCEPTION
    garb = pd.concat([garb, _asm]).drop_duplicates(keep=False)
    log_report(_asm, '_asm')


    # === uncategorized ===
    garb_prp1 = ['Sign & Label','Plumbing Hardware','Pièce Manufacturée Magasin']
    spl, garb, _uncatego = trash_prp1(spl, garb, prp1=garb_prp1)
    garb = pd.concat([garb, _uncatego]).drop_duplicates(keep=False)
    log_report(_uncatego, '_uncatego')


    # === robot ===
    spl, garb, _robot = trash_robot(spl, garb)
    garb = pd.concat([garb, _robot]).drop_duplicates(keep=False)
    log_report(_robot, '_robot')


     # === gripper ===
    spl, garb, _inside_gripper = trash_item_number(spl, garb,
        list_parts=contents_of_gripper #The contents of gripper in the file settings.
    )
    garb = pd.concat([garb, _inside_gripper]).drop_duplicates(keep=False)
    log_report(_inside_gripper, '_inside_gripper')


    # === industrial ===
    spl, garb, _industrial= trash_prp(spl, garb,
        prp1=["Industrial Engine"],
        prp2=["Engine Parts"],
    )
    garb = pd.concat([garb, _industrial]).drop_duplicates(keep=False)
    log_report(_industrial, '_industrial')


    # === _furniture ===
    spl, garb, _furniture = trash_prp(spl, garb,
        prp1=["Factory Furniture"],
        prp2=["Tape"],
    )
    garb = pd.concat([garb, _furniture]).drop_duplicates(keep=False)
    log_report(_furniture, '_furniture')


    # === _gearbox ===
    spl, garb, _gearbox = trash_prp(spl, garb,
        prp1=["Mechanical Component"],
        prp2=["Gearbox, Gear, Rack & Pinion",
            "Gear Motor & Motor",
        ]
    )
    garb = pd.concat([garb, _gearbox ]).drop_duplicates(keep=False)
    log_report(_gearbox, '_gearbox')


    # === _sheave ===
    spl, garb, _sheave = trash_description(spl, garb,
        keyword='TIMING BELT SHEAVE'
    )
    garb = pd.concat([garb, _sheave]).drop_duplicates(keep=False)
    log_report(_sheave, '_sheave')


    # === _grommet ===
    spl, garb, _grommet = trash_description(spl, garb,
        keyword='GROMMET;RUBBER',
    )
    garb = pd.concat([garb, _grommet]).drop_duplicates(keep=False)
    log_report(_grommet, '_grommet')


    # === _manif ===
    spl, garb, _manif = trash_description(spl, garb,
        keyword=r"PNEU.VALVE\sMANIFOLD\s[\d/\d\:\d{2}|\d\:\d{2}]",
        description="description_1",
    )
    garb = pd.concat([garb, _manif]).drop_duplicates(keep=False)
    log_report(_manif, '_manif')


    # === _pneu_frl ===
    spl, garb, _pneu_frl = trash_description(spl, garb,
        keyword=r"PNEU\.F\.R\.L",
        description="description_1",
    )
    garb = pd.concat([garb, _pneu_frl]).drop_duplicates(keep=False)
    log_report(_pneu_frl, '_pneu_frl')


    # === _clamp ===
    spl, garb, _clamp = trash_description(spl, garb,
        keyword="CLAMP;TRANSPORT UNIT",
        description="description_2",
    )
    garb = pd.concat([garb, _clamp]).drop_duplicates(keep=False)
    log_report(_clamp, '_clamp')


    # === electric ===
    electric_prp1 = ['Electric Component']
    spl, garb, _elec = trash_prp(spl, garb,
        prp1=["Electric Component"],
        prp2=[
            "Cable Tray & Cable Carrier",
            "Conduits & fittings",
            "Enclosures","Sensors",
            "Lights & bulbs",
            "Switches",
            "General hardware",
            "Stickers",
            "Buttons & pilot lights",
            "Connectors & crimps",
        ]
    )
    garb = pd.concat([garb, _elec]).drop_duplicates(keep=False)
    log_report(_elec, '_elec')


    # === _par ===
    spl, garb, _par = trash_file_name(spl, garb,
        keyword = r'^par\s*$',
    )
    garb = pd.concat([garb, _par]).drop_duplicates(keep=False)
    log_report(_par, '_par')


    # === _P1_A1 ===
    spl, garb, _P1_A1 = trash_parts_ending_P1_or_A1(spl, garb)
    garb = pd.concat([garb, _P1_A1]).drop_duplicates(keep=False)
    log_report(_P1_A1, '_P1_A1')


    # === _housed_cap ===
    housed_cap = r'HOUSED.*BRG.*CAP'
    spl, garb, _housed_cap = trash_description(spl, garb,
        keyword=housed_cap,
    )
    garb = pd.concat([garb, _housed_cap]).drop_duplicates(keep=False)
    log_report(_housed_cap, '_housed_cap')


    # === _collar ===
    collar = r'COLLAR'
    spl, garb, _collar = trash_description(spl, garb,
        keyword=collar,
    )
    garb = pd.concat([garb, _collar]).drop_duplicates(keep=False)
    log_report(_collar, '_collar')


    # === fpmr ===
    fpmr = r'FIXING PLATE MOTOR ROLLER'
    spl, garb, _fpmr = trash_description(spl, garb,
        keyword=fpmr,
    )
    garb = pd.concat([garb, _fpmr]).drop_duplicates(keep=False)
    log_report(_fpmr, '_fpmr')

    # === fit ===
    fit = r'PNEU.FIT.NIPPLE'
    spl, garb, _fit = trash_description(spl, garb, keyword=fit)
    garb = pd.concat([garb, _fit]).drop_duplicates(keep=False)
    log_report(_fit, '_fit')

    # === miscellaneous ===
    rejected_parts=['DPP95A1530S-3',
            '136918',
            '216081',
            '162463',
            '146660',
            '02479',
            'EEG59F2164P-9151967',
    ]
    spl, garb, _misc = trash_item_number(spl, garb, rejected_parts)
    garb = pd.concat([garb, _misc]).drop_duplicates(keep=False)

    log_report(_misc, '_misc')

    return (spl, garb, _elec, _nuts, _plates, _asm)


