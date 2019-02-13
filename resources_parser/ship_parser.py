import json
import csv
from models import Ship, WeaponSlot, HullMod, Wing, Weapon


class ShipsParser:
    def __init__(self, engine, session, path_to_ship_data):
        self.engine = engine
        self.session = session
        self.ships_data_cache = self.create_ships_cache(path_to_ship_data)


    def __call__(self, path_to_ship_file):
        ship_data = self.get_ship_data(path_to_ship_file)
        return ship_data
        # return self.create_ship(ship_data)


    def create_ships_cache(self, path_to_ship_data):
        ship_data_cache = {}
        with open(path_to_ship_data) as ship_data_file:
            ships_data = csv.DictReader(ship_data_file)
            for line in ships_data:
                ship_name = line["name"]
                ship_data_cache[ship_name] = line
        return ship_data_cache


    def create_ship(self, ship_data):
        """WIP"""
        ship = Ship()
        """
        Эти вещи временно отключены, так как требуется сперва распарсить соответствующие категории
        if weapon_slots:
            for weapon_slot in weapon_slots:
                weapon = WeaponSlot(slot_info=weapon_slot, ship_id=ship.id)
        if built_in_mods:
            for mod_name in built_in_mods:
                mode = self.get_hull_mod_by_name(mod_name)
                ship.built_in_mods.append(mode)
        if built_in_wings:
            for wing_name in built_in_wings:
                wing = self.get_wing_by_name(wing_name)
                ship.built_in_wings.append(wing)
        if built_in_weapons:
            for weapon_id in built_in_weapons:
                weapon = self.get_weapon_by_id(weapon_id)
                ship.built_in_weapons.append(weapon)
        return ship
               ship.weapon_slots.append(weapon)
        """
        return ship


    def get_ship_data(self, path_to_ship_file):
        ship_data_from_ship_file = self.get_ship_data_from_ship_file(path_to_ship_file)
        ship_name = ship_data_from_ship_file['ship_name']
        ship_data_from_csv = self.get_ship_data_from_csv(ship_name)
        ship_data = {**ship_data_from_ship_file, **ship_data_from_csv}
        return ship_data


    def get_ship_data_from_csv(self, ship_name):
        ship_data = {}
        ship_data_csv = self.ships_data_cache[ship_name]
        for key in ship_data_csv:
            ship_data[key] = ship_data_csv[key]
        return ship_data


    def get_ship_data_from_ship_file(self, path_to_ship_file):
        with open(path_to_ship_file) as ship_file:
            ship_json = json.load(ship_file)
        ship_data = {}
        ship_data['ship_name'] = ship_json['hullName']
        ship_data['sprite_name'] = ship_json['spriteName']
        ship_data['width'] = int(ship_json['width'])
        ship_data['height'] = int(ship_json['height'])
        ship_data['hull_id'] = ship_json['hullId']
        ship_data['hull_size'] = ship_json['hullSize']
        ship_data['style'] = ship_json['style']
        ship_data['center'] = ','. join([str(coord) for coord in ship_json['center']])
        ship_data['weapon_slots'] = ship_json['weaponSlots']
        ship_data['built_in_mods'] = ship_json.get('builtInMods', None)
        ship_data['built_in_wings'] = ship_json.get('builtInWings', None)
        ship_data['built_in_weapons'] = ship_json.get('builtInWeapons', None)
        ship_data['weapon_slots'] = ship_json.get('weaponSlots', None)
        return ship_data


    def get_hull_mod_by_name(self, mod_name):
        hull_mod = self.session.query(HullMod).filter_by(hull_name=mod_name).first()
        return hull_mod


    def get_wing_by_name(self, wing_name):
        wing = self.session.query(Wing).filter_by(wing_name=wing_name).first()
        return wing


    def get_weapon_by_id(self, weapon_id):
        weapon = self.session.query(Weapon).filter_by(weapon_id=weapon_id).first()
        return weapon
