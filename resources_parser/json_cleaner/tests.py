import unittest
import json
from json_pythonizer import json_load, json_loads, remove_extra_commas, remove_python_style_comments


class TestJsonCleaner(unittest.TestCase):
    def setUp(self):
        self.path_to_dirty_json_file = './bad.json'
        self.correct_json_string = '{"a":[\n\t1,\n\t2,\n\t3],  \n"b": "B",\n\t"c":{"ca": "CA"}}\n'
        self.python_json = {'a': [1, 2, 3], 'b': 'B', 'c': {'ca': 'CA'}}

    def test_remove_extra_commas(self):
        test_string_1 = "{'a':10, b:20,}"
        test_string_2 = "{\n\t'a':10,\n}\n"
        test_string_3 = "{'a':10}"
        self.assertEqual(remove_extra_commas(test_string_1), "{'a':10, b:20}")
        self.assertEqual(remove_extra_commas(test_string_2), "{\n\t'a':10}\n")
        self.assertEqual(remove_extra_commas(test_string_3), test_string_3)

    def test_remove_python_style_comments(self):
        test_string_1 = "{'a':10 # comment \n}\n"
        test_string_2 = "{'a':10\n#comment\n}\n"
        test_string_3 = "{'a':10,\nb:20\n}\n"
        self.assertEqual(remove_python_style_comments(test_string_1), "{'a':10\n}\n")
        self.assertEqual(remove_python_style_comments(test_string_2), "{'a':10\n}\n")
        self.assertEqual(remove_python_style_comments(test_string_3), "{'a':10,\nb:20\n}\n")

    def test_json_load(self):
        cleared_string = json_load(self.path_to_dirty_json_file)
        self.assertEqual(cleared_string, self.correct_json_string)

    def test_json_loads(self):
        with open(self.path_to_dirty_json_file) as _file:
            dirty_json_string = _file.read()
        cleared_string = json_loads(dirty_json_string)
        self.assertEqual(cleared_string, self.correct_json_string)

    def test_decode_cleared_string(self):
        cleared_scring = json_load(self.path_to_dirty_json_file)
        try:
            loaded = json.loads(cleared_scring)
        except json.decoder.JSONDecodeError:
            self.fail('Cant decode string')
        self.assertEqual(loaded, self.python_json)


if __name__ == "__main__":
    unittest.main()
