import json
from sqlalchemy.orm.session import make_transient
from sqlalchemy import and_
from models import Ship, Weapon
from json_cleaner.json_cleaner import json_load_skin


class SkinParser():
    def __init__(self, session, mod_name):
        self.__session = session
        self.mod_name = mod_name

    def __call__(self, path_to_skin_file: str) -> Ship:
        skin_data = self.get_skin_data(path_to_skin_file)
        if not self.is_ship(skin_data):
            return None
        ship = self.create_ship_from_skin(skin_data)
        return ship

    def is_ship(self, ship_data: dict) -> bool:
        if not ship_data.get('skin_name'):
            return False
        return True

    def create_ship_from_skin(self, skin_data: dict) -> Ship:
        ship = self.get_base_ship(skin_data['base_hull_id'])
        self.__session.expunge(ship)
        make_transient(ship)
        ship.hull_id = skin_data['skin_id']
        ship.ship_name = skin_data['skin_name']
        ship.sprite_name = skin_data['path_to_sprite']
        if skin_data['OP']:
            ship.ordnance_points = skin_data['OP']
        ship.description = skin_data['description_prefix'] + '\n' + ship.description
        ship.weapon_slots = self.update_weapon_slots(ship.weapon_slots, skin_data['removed_weapon_slots'])
        return ship

    def update_weapon_slots(self, weapon_slots: dict, removed_weapon_slots: list) -> dict:
        for weapon_slot_id in removed_weapon_slots:
            weapon_slots.pop(weapon_slot_id)
        return weapon_slots

    def get_skin_data(self, path_to_skin_file: str) -> dict:
        skin_cleaned = json_load_skin(path_to_skin_file)
        skin_json = json.loads(skin_cleaned)
        skin_data = {}
        skin_data['base_hull_id'] = skin_json['baseHullId']
        skin_data['skin_id'] = skin_json['skinHullId']
        skin_data['skin_name'] = skin_json.get('hullName', '')
        skin_data['description_prefix'] = skin_json.get('descriptionPrefix', '')
        skin_data['OP'] = skin_json.get('ordnancePoints', None)
        skin_data['path_to_sprite'] = '/' + self.mod_name + '/' + skin_json.get('spriteName', '')
        skin_data['removed_weapon_slots'] = skin_json.get('removeWeaponSlots', [])
        skin_data['removed_weapons'] = skin_json.get('removeBuiltInWeapons', [])
        return skin_data

    def get_base_ship(self, base_hull_id: str) -> Ship:
        base_ship = self.__session.query(Ship).filter(Ship.hull_id==base_hull_id).first()
        return base_ship
