import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ship_parser import ShipsParser
from models import create_models


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

parser = ShipsParser(engine)
ship_files = ['./ships/wolf.ship']
for ship in ship_files:
    ship = parser(ship)
    session.add(ship)
session.commit()
