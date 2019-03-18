import json
import csv
from models import Ship, WeaponSlot, Weapon
from json_cleaner.json_cleaner import json_load_light
from styles import STYLES
from ignore import ignored_hulls, ignored_names


class ShipsParser:
    def __init__(self, path_to_ships_data: str, path_to_descriptions_file: str, mod_name: str):
        self.ships_data_cache = self.create_ships_cache(path_to_ships_data)
        self.descriptions = self.create_descriptions_cache(path_to_descriptions_file)
        self.mod_name = mod_name

    def __call__(self, path_to_ship_file: str) -> Ship:
        ship_data = self.get_ship_data(path_to_ship_file)
        # Проверка на то, является ли этот ship файл файлом корабля
        if not self.is_ship(ship_data):
            return None
        ship = self.create_ship(ship_data)
        return ship

    def is_ship(self, ship_data):
        if not ship_data:
            return False
        ship_name = ship_data['ship_name']
        if ship_name in ignored_names:
            return False
        if not ship_data.get('name'):
            return False
        hull_id = ship_data['hull_id']
        for hull in ignored_hulls:
            if hull_id.startswith(hull):
                return False
        return True

    def create_ships_cache(self, path_to_ships_data: str) -> dict:
        ships_data_cache = {}
        with open(path_to_ships_data) as ships_data_file:
            ships_data = csv.DictReader(ships_data_file)
            for line in ships_data:
                hull_id = line['id']
                ships_data_cache[hull_id] = line
        return ships_data_cache

    def create_descriptions_cache(self, path_to_descriptions_file: str) -> dict:
        descriptions = {}
        with open(path_to_descriptions_file) as descriptions_file:
            descriptions_data = csv.DictReader(descriptions_file)
            for line in descriptions_data:
                line_type = line['type']
                if line_type == 'SHIP':
                    hull_id = line['id']
                    descriptions[hull_id] = line['text1']
        return descriptions

    def get_ship_data(self, path_to_ship_file: str) -> dict:
        ship_data_from_ship_file = self.get_ship_data_from_ship_file(path_to_ship_file)
        hull_id = ship_data_from_ship_file['hull_id']
        ship_data_from_csv = self.get_ship_data_from_csv(hull_id)
        if not ship_data_from_csv:
            return {}
        ship_description = self.get_ship_description(hull_id)
        ship_data = {**ship_data_from_ship_file, **ship_data_from_csv, 'description': ship_description}
        return ship_data

    def get_ship_data_from_csv(self, hull_id: str) -> dict:
        ship_data = self.ships_data_cache.get(hull_id, {})
        return ship_data

    def get_ship_description(self, hull_id: str):
        ship_description = self.descriptions.get(hull_id, '')
        return ship_description

    def get_ship_style(self, ship_json):
        if self.mod_name == 'Base':
            ship_style = STYLES[ship_json['style']]
        else:
            ship_style = STYLES[self.mod_name]
        return ship_style

    def get_ship_data_from_ship_file(self, path_to_ship_file: str) -> dict:
        with open(path_to_ship_file) as ship_file:
            ship_cleaned = json_load_light(path_to_ship_file)
            ship_json = json.loads(ship_cleaned)
        ship_data = {}
        ship_data['ship_name'] = ship_json['hullName']
        ship_data['sprite_name'] = '/' + self.mod_name + '/' + ship_json['spriteName']
        ship_data['width'] = int(ship_json['width'])
        ship_data['height'] = int(ship_json['height'])
        ship_data['hull_id'] = ship_json['hullId']
        ship_data['hull_size'] = ship_json['hullSize']
        ship_data['style'] = self.get_ship_style(ship_json)
        ship_data['center'] = ','. join([str(coord) for coord in ship_json['center']])
        ship_data['built_in_mods'] = ship_json.get('builtInMods', None)
        ship_data['built_in_wings'] = ship_json.get('builtInWings', None)
        ship_data['built_in_weapons'] = ship_json.get('builtInWeapons', {})
        ship_data['weapon_slots'] = ship_json.get('weaponSlots', None)
        return ship_data

    def get_weapon_by_id(self, weapon_id: str) -> Weapon:
        weapon = self.session.query(Weapon).filter_by(weapon_id=weapon_id).first()
        return weapon

    def create_weapon_slot(self, weapon_slot: dict, ship_name: str, built_in_weapons: dict) -> WeaponSlot:
        weapon_slot_obj = WeaponSlot(slot_id = weapon_slot['id'],
                            angle = weapon_slot['angle'],
                            arc = weapon_slot['arc'],
                            mount = weapon_slot['mount'],
                            size = weapon_slot['size'],
                            slot_type = weapon_slot['type'],
                            location = ','.join([str(coord) for coord in weapon_slot['locations']]),
                            ship_name = ship_name)
        if weapon_slot['type'] == 'BUILT_IN' and weapon_slot['mount'] != 'HIDDEN':
            weapon_id = built_in_weapons[weapon_slot['id']]
            weapon_slot_obj.weapon = weapon_id
        return weapon_slot_obj

    def create_ship(self, ship_data: dict) -> Ship:
        """
        todo:
        built_in_mods
        built_in_wings
        """
        ship = Ship(
            ship_name = ship_data['ship_name'],
            sprite_name = ship_data['sprite_name'],
            width = ship_data['width'],
            height = ship_data['height'],
            hull_id = ship_data['hull_id'],
            hull_size = ship_data['hull_size'],
            style = ship_data['style'],
            center = ship_data['center'],
            armor_rating = ship_data['armor rating'],
            acceleration = ship_data['acceleration'],
            field_8_6_5_4 = ship_data['8/6/5/4%'] if ship_data['8/6/5/4%'] else 0,
            cargo = ship_data['cargo'] if ship_data['cargo'] else 0,
            deceleration = ship_data['deceleration'],
            flux_dissipation = ship_data['flux dissipation'],
            fuel = ship_data['fuel'] if ship_data['fuel'] else 0,
            fuel_ly = ship_data['fuel/ly'] if ship_data['fuel/ly'] else 0,
            hitpoints = ship_data['hitpoints'],
            mass = ship_data['mass'],
            max_crew = ship_data['max crew'] if ship_data['max crew'] else 0,
            max_flux = ship_data['max flux'],
            max_speed = ship_data['max speed'],
            max_turn_rate = ship_data['max turn rate'],
            min_crew = ship_data['min crew'] if ship_data['min crew'] else 0,
            ordnance_points = ship_data['ordnance points'] if ship_data['ordnance points'] else 0,
            shield_arc = ship_data['shield arc'] if ship_data['shield arc'] else 0,
            shield_efficiency = ship_data['shield efficiency'] if ship_data['shield efficiency'] else 0,
            shield_type = ship_data['shield type'] if ship_data['shield type'] else 'none',
            shield_upkeep = ship_data['shield upkeep'] if ship_data['shield upkeep'] else 0,
            supplies_month = ship_data['supplies/mo'] if ship_data['supplies/mo'] else 0,
            description = ship_data['description'],
            mod_name = self.mod_name
        )
        if ship_data['weapon_slots']:
            built_in_weapons = ship_data.get('built_in_weapons', {})
            for weapon_slot in ship_data['weapon_slots']:
                weapon = self.create_weapon_slot(weapon_slot, ship.ship_name, built_in_weapons)
                ship.weapon_slots.append(weapon)
        return ship
