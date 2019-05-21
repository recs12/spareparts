
from loguru import logger
from spareparts.lib.dispatch import *
from spareparts.lib.settings import *

logger.add("report_{time}.log", level="INFO") ##log to be tested

def strain(spl, garb):
    #prp1 arguments
    plates_prp1 = ['Aluminium','Stainless Steel','Steel']
    spl, garb, _plate = trash_prp1(
            spl,
            garb,
            prp1=plates_prp1,
    )
    logger.info("_plate:\n" + _plate[['part_number','description_1']].to_string())
    
    #bolts arguments in prp1
    boulonnerie_prp1 = ['Inch Fastener','Inch Hardware','Metric Fastener','Metric Hardware']
    spl, garb, _nuts = trash_prp1(
            spl,
            garb,
            prp1=boulonnerie_prp1,
    )
    logger.info("_nuts:\n" + _nuts[['part_number','description_1']].to_string())
    garb = pd.concat([garb, _nuts]).drop_duplicates(keep=False) #TODO: add _nuts into new tab
    spl, garb, _asm = trash_assemblies(spl, garb)
    logger.info(_asm[['part_number','description_1']].to_string())

    spl, garb, _garb = trash_prp1(
            spl,
            garb,
            prp1=garb_prp1,
    )

    spl, garb, _robot = trash_robot(spl, garb)
    logger.info("_robot:\n" + _robot[['part_number','description_1']].to_string())
    
    spl, garb, _inside_gripper = trash_item_number(
        spl,
        garb,
        list_parts=contents_of_gripper
    )
    spl, garb, _industrial= trash_prp(
        spl,
        garb,
        prp1=["Industrial Engine"],
        prp2=["Engine Parts"],
    )
    spl, garb, _furniture = trash_prp(
        spl,
        garb,
        prp1=["Factory Furniture"],
        prp2=["Tape"]
    )
    spl, garb, _gearbox = trash_prp(
        spl,
        garb,
        prp1=["Mechanical Component"],
        prp2=[
            "Gearbox, Gear, Rack & Pinion",
            "Cable Tray & Cable Carrier",
            "Clutch, Brake & Torque Limiter",
            "Gear Motor & Motor",
        ]
    )
    spl, garb, _quincaillery = trash_prp(
        spl,
        garb,
        prp1=["Mechanical Component"],
        prp2=[  "Quincaillery",
                "Chain & Sprocket",
        ]
    )
    spl, garb, _sheave = trash_description(
        spl,
        garb,
        keyword='TIMING BELT SHEAVE'
    )
    spl, garb, _grommet = trash_description(
        spl,
        garb,
        keyword='GROMMET;RUBBER'
    )
    spl, garb, _manif = trash_description(
        spl,
        garb,
        keyword="PNEU.VALVE\sMANIFOLD\s[\d/\d\:\d{2}|\d\:\d{2}]",
        description="description_1"
    )
    spl, garb, _pneu_frl = trash_description(
        spl,
        garb,
        keyword="PNEU\.F\.R\.L",
        description="description_1"
    )
    spl, garb, _clamp = trash_description(
        spl,
        garb,
        keyword="CLAMP;TRANSPORT UNIT",
        description="description_2"
    )
    #spl, garb, _sig = adjust_significance_notnull(spl, garb) #-> deactivated
    #electric components
    electric_prp1 = ['Electric Component']
    spl, garb, _elec = trash_prp(
        spl,
        garb,
        prp1=["Electric Component"],
        prp2=[
            "Cable Tray & Cable Carrier",
            "Conduits & fittings",
            "Enclosures","Sensors",
            "Lights & bulbs",
            "Switches",
            "General hardware",
            "Stickers",
        ]
    )
    spl, garb, _par = trash_file_name(
        spl,
        garb,
        keyword = r'^par\s*$'
    )
    spl, garb, _P1_A1 = trash_parts_ending_P1_or_A1(spl, garb)

    #remove the housed cap
    #HOUSED BRG.CAP
    housed_cap = r'HOUSED.*BRG.*CAP'
    spl, garb, _housed_cap = trash_description(
            spl,
            garb,
            keyword=housed_cap,
    )
    #remove collars
    collar = r'COLLAR'
    spl, garb, _collar = trash_description(
            spl,
            garb,
            keyword=collar,
    )
    #remove FIXING PLATE MOTOR ROLLER
    fpmr = r'FIXING PLATE MOTOR ROLLER'
    spl, garb, _collar = trash_description(
            spl,
            garb,
            keyword=fpmr,
    )
    # tfile = open('steel.log', 'a')
    # tfile.write(_plate['part_number'].to_string())
    # tfile.close()
    return (spl, garb) #(spl, garb, report)



#-----FILTRES FOR SPL--------------------

#divers arguments for parts not needed in the spl.
garb_prp1 = ['Sign & Label','Synthetic Product','Plumbing Hardware','Pièce Manufacturée Magasin']


