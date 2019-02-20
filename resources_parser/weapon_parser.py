import json
import csv
from json_cleaner.json_cleaner import json_load
from models import Weapon


class WeaponsParser:
    def __init__(self, path_to_weapons_data: str, path_to_descriptions_file: str):
        self.weapon_data_cache = self.create_weapons_cache(path_to_weapons_data)
        self.descriptions = self.create_descriptions_cache(path_to_descriptions_file)

    def __call__(self, path_to_weapon_file: str) -> Weapon:
        weapon_data = self.get_weapon_data(path_to_weapon_file)
        weapon = self.create_weapon(weapon_data)
        return weapon

    def create_weapons_cache(self, path_to_weapons_data: str) -> dict:
        weapons_data_cache = {}
        with open(path_to_weapons_data) as weapons_data_file:
            weapons_data = csv.DictReader(weapons_data_file)
            for line in weapons_data:
                weapon_id = line['id']
                weapons_data_cache[weapon_id] = line
        return weapons_data_cache

    def create_descriptions_cache(self, path_to_descriptions_file: str) -> dict:
        descriptions = {}
        with open(path_to_descriptions_file) as descriptions_file:
            descriptions_data = csv.DictReader(descriptions_file)
            for line in descriptions_data:
                line_type = line['type']
                if line_type == 'WEAPON':
                    weapon_id = line['id']
                    descriptions[weapon_id] = line['text1']
        return descriptions

    def get_weapon_data(self, path_to_weapon_file: str) -> dict:
        weapon_data_from_weapon_file = self.get_weapon_data_from_weapon_file(path_to_weapon_file)
        weapon_id = weapon_data_from_weapon_file['weapon_id']
        weapon_description = self.descriptions.get(weapon_id, '')
        weapon_data_from_csv = self.get_weapon_data_from_csv(weapon_id)
        weapon_data = {**weapon_data_from_csv, **weapon_data_from_weapon_file, 'description': weapon_description}
        return weapon_data

    def get_weapon_data_from_csv(self, weapon_id: str) -> dict:
        weapon_data = self.weapon_data_cache[weapon_id]
        return weapon_data

    def get_weapon_data_from_weapon_file(self, path_to_file: str) -> dict:
        weapon_cleared = json_load(path_to_file)
        weapon_json = json.loads(weapon_cleared)
        weapon_data = {}
        weapon_data['weapon_id'] = weapon_json['id']
        weapon_data['spec_class'] = weapon_json['specClass']
        weapon_data['type'] = weapon_json['type']
        weapon_data['size'] = weapon_json['size']
        weapon_data['turret_sprite'] = weapon_json.get('turretSprite', '')
        weapon_data['hardpoint_sprite'] = weapon_json.get('hardpointSprite', '')
        autocharge = weapon_json.get('autocharge', False)
        weapon_data['autocharge'] = True if autocharge else False
        req_full_charge = weapon_json.get('requiresFullCharge', False)
        weapon_data['requires_full_charge'] = True if req_full_charge else False
        return weapon_data

    def create_weapon(self, weapon_data: dict) -> Weapon:
        weapon = Weapon(
            weapon_id = weapon_data['weapon_id'],
            weapon_name = weapon_data['name'],
            ops = weapon_data['OPs'] if weapon_data['OPs'] else 0,
            ammo = weapon_data['ammo'] if weapon_data['ammo'] else 0,
            ammo_sec = weapon_data['ammo/sec'] if weapon_data['ammo/sec'] else 0,
            autocharge = weapon_data['autocharge'],
            burst_size = weapon_data['burst size'] if weapon_data['burst size'] else 0,
            damage_sec = weapon_data['damage/second'] if weapon_data['damage/second'] else 0,
            damage_shot = weapon_data['damage/shot'] if weapon_data['damage/shot'] else 0,
            emp = weapon_data['emp'] if weapon_data['emp'] else 0,
            energy_second = weapon_data['energy/second'] if weapon_data['energy/second'] else 0,
            energy_shot = weapon_data['energy/shot'] if weapon_data['energy/shot'] else 0,
            hardpoint_sprite = weapon_data['hardpoint_sprite'],
            weapon_range = weapon_data['range'] if weapon_data['range'] else 0,
            requires_full_charge = weapon_data['requires_full_charge'],
            size = weapon_data['size'],
            spec_class = weapon_data['spec_class'],
            turn_rate = weapon_data['turn rate'] if weapon_data['turn rate'] else 0,
            turret_sprite = weapon_data['turret_sprite'],
            proj_speed = weapon_data['proj speed'] if weapon_data['proj speed'] else 0,
            weapon_type = weapon_data['type'],
            description = weapon_data['description']
        )
        return weapon
