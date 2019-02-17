import shutil
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_models, Ship
from ship_parser import ShipsParser
from weapon_parser import WeaponsParser


try:
    PATH_TO_GAME = sys.argv[1]
except IndexError:
    PATH_TO_GAME = os.path.expanduser('~/Starsector/')
PATH_TO_STATIC = os.path.expanduser('~/Dev/starsector-fitting/starsector/fitting/static/fitting/')


engine = create_engine("postgresql+psycopg2://admiral:fleet@localhost/starsector",  isolation_level="READ UNCOMMITTED")
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


def insert_or_update(ship):
    existing_ship = session.query(Ship).filter(Ship.ship_name == ship.ship_name).first()
    if not existing_ship:
        session.add(ship)
    else:
        for weapon_slots in existing_ship.weapon_slots:
            session.delete(weapon_slots)
        session.merge(ship)
    return ship


def copy_sprite_to_static(ship):
    sprite_path = PATH_TO_GAME + ship.sprite_name
    dist_path = PATH_TO_STATIC + ship.sprite_name
    dir_name, _ = os.path.split(dist_path)
    os.makedirs(dir_name, exist_ok=True)
    shutil.copyfile(sprite_path, dist_path)


create_models(engine)


ships_csv = './ships/ship_data.csv'
ship_files = ['./ships/wolf.ship', './ships/condor.ship', './ships/eagle.ship']


try:
    ships_parser = ShipsParser(ships_csv)
    for ship_file in ship_files:
        ship = ships_parser(ship_file)
        ship = insert_or_update(ship)
        copy_sprite_to_static(ship)
    session.commit()
finally:
    connection.close()
