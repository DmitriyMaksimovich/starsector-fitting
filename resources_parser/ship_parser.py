import json
from models import Ship, WeaponSlot, HullMod, Wing, Weapon


class ShipsParser:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

    def __call__(self, ship_file):
        return self.parse_ship_file(ship_file)

    def parse_ship_file(self, path_to_file):
        with open(path_to_file) as ship_file:
            ship_json = json.load(ship_file)
            ship = Ship(ship_name=ship_json['hullName'],
                        sprite_name=ship_json['spriteName'],
                        width=int(ship_json['width']),
                        height=int(ship_json['height']),
                        hull_id=ship_json['hullId'],
                        hull_size=ship_json['hullSize'],
                        style=ship_json['style'],
                        center=','.join([str(coord) for coord in ship_json['center']]))
            weapon_slots = ship_json['weaponSlots']
            for weapon_slot in weapon_slots:
                weapon = WeaponSlot(slot_info=weapon_slot, ship_id=ship.id)
                ship.weapon_slots.append(weapon)
            builtInMods = ship_json.get('builtInMods', None)
            if builtInMods:
                for mod_name in builtInMods:
                    mode = self.get_hull_mod_by_name(mod_name)
                    ship.builtInMods.append(mode)
            builtInWings = ship_json.get('builtInWings', None)
            if builtInWings:
                for wing_name in builtInWings:
                    wing = self.get_wing_by_name(wing_name)
                    ship.builtInWings.append(wing)
            builtInWeapons = ship_json.get('builtInWeapons', None)
            if builtInWeapons:
                for weapon_id in builtInWeapons:
                    weapon = self.get_weapon_by_id(weapon_id)
                    ship.builtInWeapons.append(weapon)
        return ship

    def get_hull_mod_by_name(self, mod_name):
        hull_mod = self.session.query(HullMod).filter_by(hull_name=mod_name).first()
        return hull_mod

    def get_wing_by_name(self, wing_name):
        wing = self.session.query(Wing).filter_by(wing_name=wing_name).first()
        return wing

    def get_weapon_by_id(self, weapon_id):
        weapon = self.session.query(Weapon).filter_by(weapon_id=weapon_id).first()
        return weapon
