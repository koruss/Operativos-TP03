import json
import os
import string

def write_to_json(json_file):
    '''Escribe a un archivo json.'''
    fname = "fs.json"
    directory = os.path.dirname(__file__)
    abs_dir = os.path.join(directory, '..', fname)
    with open(abs_dir, "w", encoding='UTF-8') as outfile:
        json.dump(json_file, outfile)
    return

def read_from_json():
    '''Lee de un archivo json.'''
    fname = "fs.json"
    directory = os.path.dirname(__file__)
    abs_dir = os.path.join(directory, '..', fname)
    with open(abs_dir, 'r', encoding='UTF-8') as openfile:
        json_file = json.load(openfile)
    return json_file

def file_exists():
    '''Revisa si el archivo del FS existe, para poder crear permanencia de datos'''
    fname = "fs.json"
    directory = os.path.dirname(__file__)
    abs_dir = os.path.join(directory, '..', fname)
    if os.path.isfile(abs_dir):
        return True
    return False

def name_is_valid(name):
    '''revisa si el nombre del archivo es valido'''
    invalid_chars = set(string.punctuation.replace(" ", ""))
    return not any(char in invalid_chars for char in name)
