import shutil
import os
import sys
import json
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_models, Ship, Weapon
from ship_parser import ShipParser
from weapon_parser import WeaponParser
from skin_parser import SkinParser
from json_cleaner import json_cleaner
from ignore import ignored_mods


HULLS_SUBFOLDER = '/data/hulls/'
SKINS_SUBFOLDER = HULLS_SUBFOLDER + 'skins/'
WEAPONS_SUBFOLDER = '/data/weapons/'
DESCRIPTIONS_SUBFOLDER = '/data/strings/descriptions.csv'
try:
    PATH_TO_STATIC = sys.argv[1]
except:
    PATH_TO_STATIC = os.path.expanduser('~/Dev/starsector-fitting/starsector/fitting/static/fitting/')


def insert_or_update_ship(ship: Ship, session) -> Ship:
    existing_ship = session.query(Ship).filter(Ship.ship_name == ship.ship_name).first()
    if not existing_ship:
        session.add(ship)
    else:
        for weapon_slots in existing_ship.weapon_slots:
            session.delete(weapon_slots)
        session.merge(ship)
    return ship


def insert_or_update_weapon(weapon: Weapon, session) -> Weapon:
    existing_weapon = session.query(Weapon).filter(Weapon.weapon_id == weapon.weapon_id).first()
    if not existing_weapon:
        session.add(weapon)
    else:
        session.merge(weapon)
    return weapon


def copy_ship_sprite_to_static(ship: Ship, path_to_game: str):
    ship_sprite = re.sub('^/[^/]+/', '/', ship.sprite_name)
    path_to_sprite = path_to_game + ship_sprite
    dist_path = PATH_TO_STATIC + ship.sprite_name
    dir_name, _ = os.path.split(dist_path)
    os.makedirs(dir_name, exist_ok=True)
    shutil.copyfile(path_to_sprite, dist_path)


def copy_weapon_sprites_to_static(weapon: Weapon, path_to_game: str):
    if weapon.turret_sprite:
        turret_sprite = re.sub('^/[^/]+/', '/', weapon.turret_sprite)
        path_to_sprite = path_to_game + turret_sprite
        if not os.path.isfile(path_to_sprite):
            path_to_sprite = re.sub('/mods/[^/]+/', '/', path_to_sprite)
        turret_dist_path = PATH_TO_STATIC + weapon.turret_sprite
        dir_name, _ = os.path.split(turret_dist_path)
        os.makedirs(dir_name, exist_ok=True)
        shutil.copyfile(path_to_sprite, turret_dist_path)
    if weapon.hardpoint_sprite:
        hardpoint_sprite = re.sub('^/[^/]+/', '/', weapon.hardpoint_sprite)
        path_to_sprite = path_to_game + hardpoint_sprite
        if not os.path.isfile(path_to_sprite):
            path_to_sprite = re.sub('/mods/[^/]+/', '/', path_to_sprite)
        hardpoint_dist_path = PATH_TO_STATIC + weapon.hardpoint_sprite
        dir_name, _ = os.path.split(hardpoint_dist_path)
        os.makedirs(dir_name, exist_ok=True)
        shutil.copyfile(path_to_sprite, hardpoint_dist_path)


def get_mods_folders(path_to_game: str) -> dict:
    mods = {'Base': path_to_game}
    mods_folders = [path_to_game + '/mods/' + f for f in os.listdir(path_to_game + '/mods/') if os.path.isdir(path_to_game + '/mods/' + f)]
    for mod in mods_folders:
        if 'mod_info.json' in os.listdir(mod):
            path_to_mod_info = mod + '/mod_info.json'
            mod_info_json = json.loads(json_cleaner.json_load(path_to_mod_info))
            mod_name = mod_info_json['name']
            if mod_name in ignored_mods:
                continue
            mods[mod_name] = mod
    return mods


def parse_weapon_files(path_to_game: str, mod_name: str) -> list:
    weapons = []
    path_to_weapons = path_to_game + WEAPONS_SUBFOLDER
    if not os.path.isdir(path_to_weapons):
        return weapons
    weapon_csv = path_to_game + '/data/weapons/weapon_data.csv'
    path_to_descriptions = path_to_game + DESCRIPTIONS_SUBFOLDER
    weapon_parser = WeaponParser(weapon_csv, path_to_descriptions, mod_name)
    weapon_files = [os.path.join(path_to_weapons, f) for f in os.listdir(path_to_weapons) if os.path.isfile(os.path.join(path_to_weapons, f)) and f.endswith('.wpn')]
    for weapon_file in weapon_files:
        weapon = weapon_parser(weapon_file)
        if not weapon or weapon.weapon_type == 'DECORATIVE':
            continue
        weapons.append(weapon)
    return weapons


def parse_hull_files(path_to_game: str, mod_name: str) -> list:
    ships = []
    path_to_hulls = path_to_game + HULLS_SUBFOLDER
    if not os.path.isdir(path_to_hulls):
        return ships
    ships_csv = path_to_game + '/data/hulls/ship_data.csv'
    path_to_descriptions = path_to_game + DESCRIPTIONS_SUBFOLDER
    ships_parser = ShipParser(ships_csv, path_to_descriptions, mod_name)
    ship_files = [os.path.join(path_to_hulls, f) for f in os.listdir(path_to_hulls) if os.path.isfile(os.path.join(path_to_hulls, f)) and f.endswith('.ship')]
    for ship_file in ship_files:
        ship = ships_parser(ship_file)
        if not ship:
            continue
        ships.append(ship)
    return ships


def parse_skin_files(path_to_game: str, mod_name, session) -> list:
    ship_skins = []
    path_to_skins = path_to_game + SKINS_SUBFOLDER
    if not os.path.isdir(path_to_skins):
        return ship_skins
    skin_parser = SkinParser(session, mod_name)
    skin_files = [os.path.join(path_to_skins, f) for f in os.listdir(path_to_skins) if os.path.isfile(os.path.join(path_to_skins, f)) and f.endswith('.skin')]
    for skin_file in skin_files:
        ship_skin = skin_parser(skin_file)
        if not ship_skin:
            continue
        ship_skins.append(ship_skin)
    return ship_skins


if __name__ == '__main__':
    try:
        path_to_game = sys.argv[2]
    except IndexError:
        path_to_game = os.path.expanduser('~/Starsector')

    ENGINE = create_engine("postgresql+psycopg2://admiral:fleet@localhost/starsector", isolation_level="READ UNCOMMITTED")
    create_models(ENGINE)

    with ENGINE.connect() as connection:
        Session = sessionmaker(bind=ENGINE)
        session = Session()

        mods = get_mods_folders(path_to_game)
        for mod in mods:
            weapons = parse_weapon_files(mods[mod], mod)
            for weapon in weapons:
                copy_weapon_sprites_to_static(weapon, mods[mod])
                _ = insert_or_update_weapon(weapon, session)
            session.commit()
            ships = parse_hull_files(mods[mod], mod)
            for ship in ships:
                copy_ship_sprite_to_static(ship, mods[mod])
                _ = insert_or_update_ship(ship, session)
            session.commit()
            ship_skins = parse_skin_files(mods[mod], mod, session)
            for ship_skin in ship_skins:
                copy_ship_sprite_to_static(ship_skin, mods[mod])
                _ = insert_or_update_ship(ship_skin, session)
            session.commit()
