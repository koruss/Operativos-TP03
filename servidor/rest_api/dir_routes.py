# Imports
from rest_api import app
from flask import request, jsonify, make_response
from storage_manager.file_manager import get_directory, mkdir, is_unique_dir, rm_dir, move_directory
from flask_expects_json import expects_json

post_directory = {
    "type": "object",
    "properties": {
        "newDirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["newDirPath", "dirName", "forceOverwrite"]
}

delete_dir_req_schema = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"}
    },
    "required": ["dirPath", "dirName"]
}

post_move_dir_req_schema = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "destinyPath": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["dirPath", "dirName", "destinyPath", "forceOverwrite"]
}

post_share_dir_req_schema = {
    "type": "object",
    "properties": {
        "dirPath": {"type": "string"},
        "dirName": {"type": "string"},
        "destinyUsername": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["dirPath", "dirName", "destinyUsername", "forceOverwrite"]
}

post_vv_copy_dir_req_schema = {
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
@app.route('/dirs', methods=['GET'])
def get_dir():
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
        error = {"message": "La URL dada no tiene una ruta de directorio"}
        return make_response(jsonify(error), 408)
    resp = get_directory(dir_path)
    if not resp:
        error = {"message": "La ruta del directorio seleccionado no existe"}
        return make_response(jsonify(error), 409)
    return make_response(jsonify(resp), 200)


# Route to create a directory in given path
@app.route('/dirs', methods=['POST'])
@expects_json(post_directory)
def post_dir():
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
        error = {"message": "The given directory name already exists", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = mkdir(content["newDirPath"], content["dirName"])
    if not status:
        error = {"message": "The given directory name is invalid, please try another", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["newDirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)


# Route to delete an existing directory
@app.route('/dirs', methods=['DELETE'])
@expects_json(delete_dir_req_schema)
def delete_dir():
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
        error = {"message": "The directory doesn't exist"}
        return make_response(jsonify(error), 408)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"]}
    return make_response(jsonify(resp), 200)


# Route to move a directory
@app.route('/dirs/move', methods=['POST'])
@expects_json(post_move_dir_req_schema)
def move_dir():
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
        error = {"message": "Another directory already exists at the shared directory of the target user",
                 "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = move_directory(content["dirPath"], content["dirName"], content["destinyPath"])
    if not status:
        error = {"message": "The directory could not be moved", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)


# Route to share a directory with another user
@app.route('/dirs/share', methods=['POST'])
@expects_json(post_share_dir_req_schema)
def share_dir():
    """
    response:
    {
        "sourceUsername": String
        "destinyUsername": String,
        "sharedDirName": String
    }
    """
    content = request.json
    if not is_unique_dir(content["destinyUsername"] + "/shared", content["dirName"]) and not content["forceOverwrite"]:
        error = {"message": "Another directory already exists at the shared folder of target user",
                 "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = 'gay'
    if not status:
        error = {"message": "The directory could not be shared", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"destinyUsername": content["destinyUsername"], "sharedFileName": content["dirName"],
            "requestOverwrite": False}
    return make_response(jsonify(resp), 200)


# Route to make a vv copy of a dir
@app.route('/dirs/vvcopy', methods=['POST'])
@expects_json(post_vv_copy_dir_req_schema)
def vv_copy_dir():
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
        error = {"message": "The given directory name already exists at target location", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = True
    if not status:
        error = {"message": "The directory could not be copied", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"dirName": content["dirName"], "dirPath": content["dirPath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)
