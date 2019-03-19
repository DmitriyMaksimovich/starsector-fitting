import csv


class ShipsCache:
    def __init__(self, path_to_ships_data: str, path_to_descriptions_file: str):
        self.ships_data_cache = self.create_ships_cache(path_to_ships_data)
        self.descriptions = self.create_descriptions_cache(path_to_descriptions_file)

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

