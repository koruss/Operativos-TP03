import os
from storage_manager.json_manager import write_to_json, read_from_json, file_exists
from storage_manager.virtual_disk_manager import create_virtual_disk

def get_space_info(username):
    json = read_from_json(username)
    return json["total_space"], json["used_space"]

def mk_fs(sec_size, sec_amnt):
    '''Función que crea un nuevo filesystem que se guarda en formato json.'''
    json = {
        "sector_size": sec_size,
        "sector_amount": sec_amnt,
        "total_space": (sec_size*sec_amnt),
        "used_space": 0,
        "root": {
            "name": "root",
            "directories": [],
            "files": []
        }
    }
    return json

def create_fs(sec_size, sec_amnt):
    '''Crea un filesystem nuevo si no existe.'''
    if not file_exists():
        # Primero crear el json.
        json = mk_fs(sec_size, sec_amnt)
        write_to_json(json)
        # Después crear el archivo de disco virtual.
        create_virtual_disk(sec_amnt, sec_size)
        return True
    return False
