
# nuts, assemblies, plates, divers, robot, grommet, factory_furniture,industrial, pneumatic, par, timing_belt_sheave, cable_carrier, motor_shrink_disk, gearmotor_servomotor, gearbox, clamps, quincaillery, pneu_frl, pneu_manifold, inside_gripper
from spareparts.lib.dispatch import *
from spareparts.lib.settings import *

def strain(spl, garb):
    spl, garb, _plate = trash_prp1(
            spl, 
            garb, 
            prp1=plates_prp1,
    )
    spl, garb, _nuts = trash_prp1(
            spl, 
            garb, 
            prp1=boulonnerie_prp1, 
    )
    spl, garb, _asm = trash_assemblies(spl, garb)
    spl, garb, _garb = trash_prp1(
            spl, 
            garb, 
            prp1=garb_prp1, 
    )
    spl, garb, _robot = trash_robot(spl, garb)
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
            "Gear Motor & Motor"
        ]
    )
    spl, garb, _quincaillery = trash_prp(
        spl,
        garb,
        prp1=["Mechanical Component"],
        prp2=["Quincaillery"]
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
    spl, garb, _sig = adjust_significance_notnull(spl, garb)
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
            "General hardware"
        ]
    )
    spl, garb, _par = trash_file_name(
        spl, 
        garb, 
        keyword = r'^par\s*$'
    )
    spl, garb, _P1_A1 = trash_parts_ending_P1_or_A1(spl, garb)

    # report = [rpt for rpt in vars(list) if rpt.startwith('rpt_')]
    return (spl, garb) #(spl, garb, report)