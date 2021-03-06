import json
import csv
from models import Ship, Weapon
from ship_cache import ShipsCache
from json_cleaner.json_cleaner import json_load_light
from styles import STYLES
from ignore import ignored_hulls, ignored_names


class ShipParser(ShipsCache):
    def __init__(self, path_to_ships_data: str, path_to_descriptions_file: str, mod_name: str):
        self.mod_name = mod_name
        super(ShipParser, self).__init__(path_to_ships_data, path_to_descriptions_file)

    def __call__(self, path_to_ship_file: str) -> Ship:
        ship_data = self.get_ship_data(path_to_ship_file)
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
        ship_data['center'] = ship_json['center']
        ship_data['built_in_mods'] = ship_json.get('builtInMods', None)
        ship_data['built_in_wings'] = ship_json.get('builtInWings', None)
        built_in_weapons = ship_json.get('builtInWeapons', {})
        weapon_slots = ship_json.get('weaponSlots', [])
        ship_data['weapon_slots'] = self.create_weapon_slots_dict(weapon_slots, built_in_weapons)
        return ship_data

    def create_weapon_slots_dict(self, weapon_slots_list: list, built_in_weapons: dict) -> dict:
        weapon_slots = {}
        for weapon_slot in weapon_slots_list:
            slot_id = weapon_slot.pop('id')
            weapon_slots[slot_id] = weapon_slot
        for slot_id in built_in_weapons:
            weapon_slots[slot_id]['weapon_id'] = built_in_weapons[slot_id]
        return weapon_slots

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
            fighter_bays = ship_data['fighter bays'] if ship_data['fighter bays'] else 0,
            max_burn = ship_data['max burn'] if ship_data['max burn'] else 0,
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
            weapon_slots = ship_data['weapon_slots'],
            description = ship_data['description'],
            mod_name = self.mod_name
        )
        return ship
