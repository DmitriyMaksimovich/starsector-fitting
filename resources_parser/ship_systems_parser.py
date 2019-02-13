import json
from models import ShipSystem


class ShipSystemParser:
    def __init__(self, engine):
        self.engine = engine

    def __call__(self, ship_system_file):
        return self.parse_ship_system_file(ship_system_file)

    def parse_ship_system_file(self, path_to_file):
        with open(path_to_file) as ship_system_file:
            ship_system_json = json.load(ship_system_file)
            ship_system = ShipSystem(system_id=ship_system_json['id'],
                                     system_type=ship_system_json['type'],
                                     ai_type=ship_system_json['aiType'])
        return ship_system
