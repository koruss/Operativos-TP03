# Imports
from flask import Flask

# Server declaration
app = Flask(__name__)

# Routes imports
import rest_api.fs_routes
import rest_api.dir_routes
import rest_api.file_routes