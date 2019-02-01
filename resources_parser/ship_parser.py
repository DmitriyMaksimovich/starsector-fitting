import json
from models import Ship, WeaponSlot


class ShipsParser:
    def __init__(self, engine):
        self.engine = engine

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
            # builtInMods = ','.join(ship_json.get('builtInMods', ''))
            # builtInWings = ','.join(ship_json.get('builtInWings', ''))
            # builtInWeapons = ','.join(ship_json.get('builtInWeapons', ''))
            # builtInMods=builtInMods,
            # builtInWings=builtInWings,
            # builtInWeapons=builtInWeapons)
        return ship
