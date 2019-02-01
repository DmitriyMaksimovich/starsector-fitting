import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_models
from ship_parser import ShipsParser
from weapon_parser import WeaponsParser


try:
    PATH_TO_GAME = sys.argv[1]
except IndexError:
    PATH_TO_GAME = './ships/'
PATH_TO_MODES = PATH_TO_GAME + "mods/"
PATH_TO_VANILA_RESOURCES = PATH_TO_GAME + "data/"

engine = create_engine('mysql+mysqldb://root:dontuse@localhost/starsector')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

create_models(engine)

ships_parser = ShipsParser(engine, session)
ship_files = ['./ships/wolf.ship']
for ship_file in ship_files:
    ship = ships_parser(ship_file)
    session.add(ship)
session.commit()

weapon_parser = WeaponsParser(engine)
weapon_files = ['./ships/amblaster.wpn']
for weapon_file in weapon_files:
    weapon = weapon_parser(weapon_file)
    session.add(weapon)
session.commit()
