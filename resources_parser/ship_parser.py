import json
import csv
from models import Ship, WeaponSlot, HullMod, Wing, Weapon


class ShipsParser:
    def __init__(self, path_to_ships_data: str):
        self.ships_data_cache = self.create_ships_cache(path_to_ships_data)

    def __call__(self, path_to_ship_file: str) -> Ship:
        ship_data = self.get_ship_data(path_to_ship_file)
        ship = self.create_ship(ship_data)
        return ship

    def create_ships_cache(self, path_to_ships_data: str) -> dict:
        ship_data_cache = {}
        with open(path_to_ships_data) as ship_data_file:
            ships_data = csv.DictReader(ship_data_file)
            for line in ships_data:
                ship_name = line["name"]
                ship_data_cache[ship_name] = line
        return ship_data_cache

    def get_ship_data(self, path_to_ship_file: str) -> dict:
        ship_data_from_ship_file = self.get_ship_data_from_ship_file(path_to_ship_file)
        ship_name = ship_data_from_ship_file['ship_name']
        ship_data_from_csv = self.get_ship_data_from_csv(ship_name)
        ship_data = {**ship_data_from_ship_file, **ship_data_from_csv}
        return ship_data

    def get_ship_data_from_csv(self, ship_name: str) -> dict:
        ship_data = {}
        ship_data_csv = self.ships_data_cache[ship_name]
        for key in ship_data_csv:
            ship_data[key] = ship_data_csv[key]
        return ship_data

    def get_ship_data_from_ship_file(self, path_to_ship_file: str) -> dict:
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

    def get_hull_mod_by_name(self, mod_name: str) -> HullMod:
        hull_mod = self.session.query(HullMod).filter_by(hull_name=mod_name).first()
        return hull_mod

    def get_wing_by_name(self, wing_name: str) -> Wing:
        wing = self.session.query(Wing).filter_by(wing_name=wing_name).first()
        return wing

    def get_weapon_by_id(self, weapon_id: str) -> Weapon:
        weapon = self.session.query(Weapon).filter_by(weapon_id=weapon_id).first()
        return weapon

    def create_weapon_slot(self, weapon_slot: dict, ship_name: str) -> WeaponSlot:
        weapon_slot_string = json.dumps(weapon_slot)
        weapon = WeaponSlot(slot_info=weapon_slot_string, ship_name=ship_name)
        return weapon

    def create_ship(self, ship_data: dict) -> Ship:
        """WIP"""
        ship = Ship(
            ship_name = ship_data['ship_name'],
            sprite_name = ship_data['sprite_name'],
            width = ship_data['width'],
            height = ship_data['height'],
            hull_id = ship_data['hull_id'],
            hull_size = ship_data['hull_size'],
            style = ship_data['style'],
            center = ship_data['center'],
            # built_in_mods = None,
            # built_in_wings = None,
            # built_in_weapons = None,
            armor_rating = ship_data['armor rating'],
            acceleration = ship_data['acceleration'],
            field_8_6_5_4 = ship_data['8/6/5/4%'],
            cargo = ship_data['cargo'],
            deceleration = ship_data['deceleration'],
            flux_dissipation = ship_data['flux dissipation'],
            fuel = ship_data['fuel'],
            fuel_ly = ship_data['fuel/ly'],
            hitpoints = ship_data['hitpoints'],
            mass = ship_data['mass'],
            max_crew = ship_data['max crew'],
            max_flux = ship_data['max flux'],
            max_speed = ship_data['max speed'],
            max_turn_rate = ship_data['max turn rate'],
            min_crew = ship_data['min crew'],
            ordnance_points = ship_data['ordnance points'],
            shield_arc= ship_data['shield arc'],
            shield_efficiency = ship_data['shield efficiency'],
            shield_type = ship_data['shield type'],
            shield_upkeep = ship_data['shield upkeep'],
            supplies_month = ship_data['supplies/mo']
        )
        if ship_data['weapon_slots']:
            for weapon_slot in ship_data['weapon_slots']:
                weapon = self.create_weapon_slot(weapon_slot, ship.ship_name)
                ship.weapon_slots.append(weapon)
        """
        Эти вещи временно отключены, так как требуется сперва распарсить соответствующие категории
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
