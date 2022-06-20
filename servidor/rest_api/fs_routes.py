from rest_api import app
from flask import request, jsonify, make_response
from flask_expects_json import expects_json
from storage_manager.fs_manager import create_fs, file_exists, get_space_info

post_fs_info_body= {
	"type": "object",
	"properties": {
		"sector_size": {"type": "number"},
		"sector_amount": {"type": "number"},
	},
	"required": ["sector_size", "sector_amount"]
}

@app.route('/fs/check', methods=['POST'])
def post_root_req():
	exists = file_exists()
	resp = {"fs_exists": exists}
	return make_response(jsonify(resp), 200)

# Crea los archivos de FS necesarios para que la progra funcione.
@app.route('/fs/create', methods=['POST'])
@expects_json(post_fs_info_body)
def post_drive_info_req():
	"""
	{
		"sector_size": Number,
		"sector_amount": Number
	}
	"""
	content = request.json
	exists = file_exists()
	if not type(content["sector_size"]) == int:
		error = {"message": "Por favor ingrese un tamaño de sector válido."}
		return make_response(jsonify(error), 409)
	if not type(content["sector_amount"]) == int:
		error = {"message": "Por favor ingrese un número de sectores válido."}
		return make_response(jsonify(error), 409)
	if exists:
		error = {"message": "Ya existe un archivo de sistema de archivos."}
		return make_response(jsonify(error), 409)
	status = create_fs(content["sector_size"], content["sector_amount"])
	resp = {"sector_size": content["sector_size"], "sector_amount":content["sector_amount"], "completed": status}
	return make_response(jsonify(resp), 200)

