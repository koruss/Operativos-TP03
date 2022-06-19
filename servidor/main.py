# Imports
from rest_api import app
from storage_manager.fs_manager import *
from storage_manager.file_manager import *

# Server start
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)





