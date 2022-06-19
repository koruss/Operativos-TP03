from rest_api import app
from flask import jsonify, make_response
from storage_manager.json_manager import file_exists

@app.route('/', methods=['POST'])
def post_root():
	exists = file_exists()
	resp = {"fs_exists": exists}
	return make_response(jsonify(resp), 200)