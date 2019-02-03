import re


def remove_extra_commas(json_string):
    cleared_json = re.sub(',\s*}', '}', json_string)
    cleared_json = re.sub(',\s*]', ']', cleared_json)
    return cleared_json


def remove_python_style_comments(json_string):
    cleared_json = re.sub('\s*#\s*[^\n]*\n', '\n', json_string)
    return cleared_json


def json_loads(json_string):
    cleared_json = remove_python_style_comments(json_string)
    cleared_json = remove_extra_commas(cleared_json)
    return cleared_json


def json_load(json_file):
    try:
        with open(json_file) as json_file:
            json_string = json_file.read()
            json_string.strip()
            cleared_json = json_loads(json_string)
        return cleared_json
    except IOError:
        print('File not found')
        return
