import shutil
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_models, Ship, Weapon
from ship_parser import ShipsParser
from weapon_parser import WeaponsParser


try:
    PATH_TO_GAME = sys.argv[1]
except IndexError:
    PATH_TO_GAME = os.path.expanduser('~/Starsector/')
PATH_TO_HULLS = PATH_TO_GAME + 'data/hulls/'
PATH_TO_WEAPONS = PATH_TO_GAME + 'data/weapons/'
PATH_TO_STATIC = os.path.expanduser('~/Dev/starsector-fitting/starsector/fitting/static/fitting/')


def insert_or_update_ship(ship):
    existing_ship = session.query(Ship).filter(Ship.ship_name == ship.ship_name).first()
    if not existing_ship:
        session.add(ship)
    else:
        for weapon_slots in existing_ship.weapon_slots:
            session.delete(weapon_slots)
        session.merge(ship)
    return ship


def insert_or_update_weapon(weapon):
    existing_weapon = session.query(Weapon).filter(Weapon.weapon_id == weapon.weapon_id).first()
    if not existing_weapon:
        session.add(weapon)
    else:
        session.merge(weapon)
    return weapon


def copy_ship_sprite_to_static(ship: Ship):
    sprite_path = PATH_TO_GAME + ship.sprite_name
    dist_path = PATH_TO_STATIC + ship.sprite_name
    dir_name, _ = os.path.split(dist_path)
    os.makedirs(dir_name, exist_ok=True)
    shutil.copyfile(sprite_path, dist_path)


def copy_weapon_sprites_to_static(weapon: Weapon):
    if weapon.turret_sprite:
        turret_sprite = PATH_TO_GAME + weapon.turret_sprite
        turret_dist_path = PATH_TO_STATIC + weapon.turret_sprite
        dir_name, _ = os.path.split(turret_dist_path)
        os.makedirs(dir_name, exist_ok=True)
        shutil.copyfile(turret_sprite, turret_dist_path)
    if weapon.hardpoint_sprite:
        hardpoint_sprite = PATH_TO_GAME + weapon.hardpoint_sprite
        hardpoint_dist_path = PATH_TO_STATIC + weapon.hardpoint_sprite
        dir_name, _ = os.path.split(hardpoint_dist_path)
        os.makedirs(dir_name, exist_ok=True)
        shutil.copyfile(hardpoint_sprite, hardpoint_dist_path)


create_models(engine)


engine = create_engine("postgresql+psycopg2://admiral:fleet@localhost/starsector",  isolation_level="READ UNCOMMITTED")
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

try:
    weapon_csv = PATH_TO_GAME + 'data/weapons/weapon_data.csv'
    weapon_files = [os.path.join(PATH_TO_WEAPONS, f) for f in os.listdir(PATH_TO_WEAPONS) if os.path.isfile(os.path.join(PATH_TO_WEAPONS, f)) and f.endswith('.wpn')]
    weapon_parser = WeaponsParser(weapon_csv)
    for weapon_file in weapon_files:
        weapon = weapon_parser(weapon_file)
        if weapon.weapon_type == 'DECORATIVE':
            continue
        weapon = insert_or_update_weapon(weapon)
        copy_weapon_sprites_to_static(weapon)

    ships_csv = PATH_TO_GAME + 'data/hulls/ship_data.csv'
    ship_files = [os.path.join(PATH_TO_HULLS, f) for f in os.listdir(PATH_TO_HULLS) if os.path.isfile(os.path.join(PATH_TO_HULLS, f)) and f.endswith('.ship')]
    ships_parser = ShipsParser(ships_csv)
    for ship_file in ship_files:
        ship = ships_parser(ship_file)
        if not ship:
            continue
        ship = insert_or_update_ship(ship)
        copy_ship_sprite_to_static(ship)
    session.commit()
finally:
    connection.close()
