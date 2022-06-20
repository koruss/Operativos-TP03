# Imports
from rest_api import app
from flask import request, jsonify, make_response
from flask_expects_json import expects_json
from storage_manager.file_manager import file_is_unique, mk_file, rm_file, modify_file, \
    get_file_unique, get_file_info, move_file, space_available_file, space_available_existing_file

# Request schemas

post_file_body = {
    "type": "object",
    "properties": {
        "filePath": {"type": "string"},
        "newFileName": {"type": "string"},
        "extension": {"type": "string"},
        "content": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["filePath", "newFileName", "extension", "content", "forceOverwrite"]
}

post_modify_file_body = {
    "type": "object",
    "properties": {
        "filePath": {"type": "string"},
        "fileName": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["filePath", "fileName", "content"]
}

post_move_file_body = {
    "type": "object",
    "properties": {
        "filePath": {"type": "string"},
        "fileName": {"type": "string"},
        "destinyPath": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["filePath", "fileName", "destinyPath", "forceOverwrite"]
}

delete_file_body = {
    "type": "object",
    "properties": {
        "filePath": {"type": "string"},
        "fileName": {"type": "string"}
    },
    "required": ["filePath", "fileName"]
}

post_vv_copy_file_body = {
    "type": "object",
    "properties": {
        "filePath": {"type": "string"},
        "fileName": {"type": "string"},
        "destinyPath": {"type": "string"},
        "forceOverwrite": {"type": "boolean"}
    },
    "required": ["filePath", "fileName", "destinyPath", "forceOverwrite"]
}

# Routes
# Route to get properties or content of a file
@app.route('/file', methods=['GET'])
def get_file():
    """
    Params:
        filePath, fileName, contentOnly
    response:
    {
        "fileName": String,
        "extension": String,
        "creation": String,
        "modification": String,
        "size": Number,
        "filePath": String,
        "content": String
    }
    if content = true, only the content field will be sent,
    otherwise response will include all fields
    """
    file_path = request.args.get('filePath')
    if file_path is None:
        error = {"message": "La dirección proporcionada no tiene el parámetro path"}
        return make_response(jsonify(error), 408)
    file_name = request.args.get('fileName')
    if file_name is None:
        error = {"message": "La dirección proporcionada no tiene el parámetro fileName"}
        return make_response(jsonify(error), 408)
    content = request.args.get('contentOnly')
    if content is None:
        error = {"message": "La dirección proporcionada no tiene el parámetro contentOnly"}
        return make_response(jsonify(error), 408)
    if content == "true":
        resp = get_file_unique(file_path, file_name)
        resp = None if resp == "" else {"content": resp}
    else:
        resp = get_file_info(file_path, file_name)
    if resp is None:
        error = {"message": "El archivo proporcionado no existe"}
        return make_response(jsonify(error), 408)
    return make_response(jsonify(resp), 200)

# Route to create a file
@app.route('/file', methods=['POST'])
@expects_json(post_file_body)
def post_file():
    """
    response:
    {
        "fileName": String,
        "filePath": String,
        "requestOverwrite": Boolean
    }
    """
    content = request.json
    if not file_is_unique(content["filePath"], content["newFileName"]) and not content["forceOverwrite"]:
        error = {"message": "Ese archivo ya existe", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    if not space_available_file(content["filePath"], content["content"]):
        error = {"message": "No hay suficiente espacio en el disco", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    status = mk_file(content["filePath"], content["newFileName"], content["extension"], content["content"])
    if not status:
        error = {"message": "El nombre proporcionado es inválido", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"fileName": content["newFileName"], "filePath": content["filePath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)

# Route to move a file
@app.route('/file/move', methods=['POST'])
@expects_json(post_move_file_body)
def move_file_req():
    """
    response:
    {
        "fileName": String,
        "filePath": String,
        "requestOverwrite": String
    }
    """
    content = request.json
    if not file_is_unique(content["destinyPath"], content["fileName"]) and not content["forceOverwrite"]:
        error = {"message": "Ya se encuentra un archivo con ese nombre en la direccion proporcionada", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = move_file(content["filePath"], content["fileName"], content["destinyPath"])
    if not status:
        error = {"message": "El archivo no se puede mover", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"fileName": content["fileName"], "filePath": content["filePath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)

# Route to modify a file
@app.route('/file/modify', methods=['POST'])
@expects_json(post_modify_file_body)
def update_file():
    """
    response:
    {
        "fileName": String,
        "path": String
    }
    """
    content = request.json
    if not space_available_existing_file(content["filePath"], content["fileName"], content["content"]):
        error = {"message": "No hay campo suficiente en memoria", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    status = modify_file(content["filePath"], content["fileName"], content["content"])
    if not status:
        error = {"message": "El archivo proporcionado no puede ser modificado"}
        return make_response(jsonify(error), 409)
    resp = {"fileName": content["fileName"], "path": content["filePath"]}
    return make_response(jsonify(resp), 200)

# Route to delete an existing file
@app.route('/file', methods=['DELETE'])
@expects_json(delete_file_body)
def delete_file():
    """
    response:
    {
        "fileName": String,
        "path": String,
    }
    """
    content = request.json
    status = rm_file(content["filePath"], content["fileName"])
    if not status:
        error = {"message": "El archivo no existe"}
        return make_response(jsonify(error), 408)
    resp = {"fileName": content["fileName"], "path": content["filePath"]}
    return make_response(jsonify(resp), 200)

# Route to make a vv copy of a file
@app.route('/file/vvcopy', methods=['POST'])
@expects_json(post_vv_copy_file_body)
def vv_copy_file():
    """
    response:
    {
        "fileName": String,
        "filePath": String,
        "requestOverwrite": Boolean
    }
    """
    content = request.json
    if not file_is_unique(content["destinyPath"], content["fileName"]) and not content["forceOverwrite"]:
        error = {"message": "Ese archivo ya existe at target location", "requestOverwrite": True}
        return make_response(jsonify(error), 409)
    status = move_file(content["filePath"], content["fileName"], content["destinyPath"], True)
    if not status:
        error = {"message": "El archivo no puede ser copiado", "requestOverwrite": False}
        return make_response(jsonify(error), 409)
    resp = {"fileName": content["fileName"], "filePath": content["filePath"], "requestOverwrite": False}
    return make_response(jsonify(resp), 200)
