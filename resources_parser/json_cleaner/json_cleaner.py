import re


def remove_extra_commas(json_string):
    cleared_json = re.sub(',\s*}', '}', json_string)
    cleared_json = re.sub(',\s*]', ']', cleared_json)
    return cleared_json


def remove_python_style_comments(json_string):
    cleared_json = re.sub('\s*#\s*[^\n]*\n', '\n', json_string)
    return cleared_json


def remove_incorrect_lists(json_string):
    cleared_json = re.sub('\[[a-zA-Z_,]+\]', '""', json_string)
    return cleared_json


def replace_semicolon_wiith_a_comma(json_string):
    cleared_json = re.sub(';\s*', ',\n', json_string)
    return cleared_json


def remove_incorrect_values(json_string):
    cleared_json = re.sub(':\s*[a-zA-Z_]+\s*', ':""\n', json_string)
    return cleared_json


def json_loads(json_string):
    cleared_json = remove_python_style_comments(json_string)
    cleared_json = remove_extra_commas(cleared_json)
    cleared_json = remove_incorrect_lists(cleared_json)
    cleared_json = replace_semicolon_wiith_a_comma(cleared_json)
    cleared_json = remove_incorrect_values(cleared_json)
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
