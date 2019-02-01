import json
from models import Weapon


class WeaponsParser:
    def __init__(self, engine):
        self.engine = engine

    def __call__(self, ship_file):
        return self.parse_weapon_file(ship_file)

    def parse_weapon_file(self, path_to_file):
        with open(path_to_file) as weapon_file:
            weapon_json = json.load(weapon_file)
            weapon = Weapon(weapon_id=weapon_json['id'],
                            spec_class=weapon_json['specClass'],
                            weapon_type=weapon_json['type'],
                            weapon_size=weapon_json['size'],
                            turret_sprite=weapon_json.get('turretSprite', None),
                            hardpoint_sprite=weapon_json.get('hardpointSprite', None))
        return weapon
