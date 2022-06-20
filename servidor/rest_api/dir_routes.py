# Imports
from rest_api import app
from flask import request, jsonify, make_response
from storage_manager.file_manager import get_directory, mkdir, is_unique_dir, rm_dir, move_directory, copy_directory_by_name
from flask_expects_json import expects_json

post_dir_body= {
    "type": "object",
    "properties": {
        "newDirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["newDirPath", "dirName", "forceOverwrite"]
}

delete_dir_body = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"}
    },
    "required": ["dirPath", "dirName"]
}

move_dir_body = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "destinyPath": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["dirPath", "dirName", "destinyPath", "forceOverwrite"]
}

vv_copy_body = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "destinyPath": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["dirPath", "dirName", "destinyPath", "forceOverwrite"]
}


# Routes
# Route to get a specific dir of an user
@app.route('/dir', methods=['GET'])
def get_dir_req():
    """
    Params:
        dirPath
    response:
    {
        "username": String,
        "contents": [
            "directories": [
                {
                    "name": String,
                    "directories": Array,
                    "files": Array
                }
            ]
            "files" [
             {
                "name": String,
                "extension": String,
                "size": Number,
                "content": String
            }
            ]
        ]
    }
    """
    dir_path = request.args.get('dirPath')
    if dir_path is None:
        error = {"message": "Directorio no especificado"}
        return make_response(jsonify(error), 408)
    resp = get_directory(dir_path)
    if not resp:
        error = {"message": "La ruta del directorio seleccionado no existe"}
        return make_response(jsonify(error), 409)
    return make_response(jsonify(resp), 200)


# Route to create a directory in given path
@app.route('/dir', methods=['POST'])
@expects_json(post_dir_body)
def post_dir_req():
    """
    response:
    {
        "dirName": String,
        "dirPath": String,
        "requestOverwrite": Boolean
    }
    """
    content = request.json
    if not is_unique_dir(content["newDirPath"], content["dirName"]) and not content["forceOverwrite"]:
        error = {"message": "El directorio ya existe", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = mkdir(content["newDirPath"], content["dirName"])
    if not status:
        error = {"message": "El nombre del directorio es inválido", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["newDirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)


# Route to delete an existing directory
@app.route('/dir', methods=['DELETE'])
@expects_json(delete_dir_body)
def delete_dir_req():
    """
    response:
    {
        "dirName": String,
        "dirPath": String,
    }
    """
    content = request.json
    status = rm_dir(content["dirPath"], content["dirName"])
    if not status:
        error = {"message": "El directorio no existe"}
        return make_response(jsonify(error), 408)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"]}
    return make_response(jsonify(resp), 200)


# Route to move a directory
@app.route('/dirs/move', methods=['POST'])
@expects_json(move_dir_body)
def move_dir_req():
    """
    response:
    {
        "dirName": String,
        "dirPath": String,
        "requestOverwrite": String
    }
    """
    content = request.json
    if not is_unique_dir(content["dirPath"], content["dirName"]) and not content["forceOverwrite"]:
        error = {"message": "Ya existe un directorio con el mismo nombre",
                 "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = move_directory(content["dirPath"], content["dirName"], content["destinyPath"])
    if not status:
        error = {"message": "No es posible mover el directorio", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)


# Route to make a vv copy of a dir
@app.route('/dirs/vvcopy', methods=['POST'])
@expects_json(vv_copy_body)
def vv_copy_dir_req():
    """
    response:
    {
        "dirName": String,
        "dirPath": String,
        "requestOverwrite": Boolean
    }
    """
    content = request.json
    if not is_unique_dir(content["destinyPath"], content["dirName"]) and not content["forceOverwrite"]:
        error = {"message": "El directorio seleccionado ya existe en la ruta especificada", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = copy_directory_by_name(content["dirPath"], content["dirName"], content["destinyPath"])
    if not status:
        error = {"message": "No es posible copiar el directorio", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)
