from fileinput import filename
from storage_manager.json_manager import *
from storage_manager.virtual_disk_manager import insert_virtual_disk , insert_virtual_disk, delete_data_virtual_disk
import datetime

def get_directory(path):
    folders = path.split("/")
    jsonObject = read_from_json()
    return get_content_from_path(folders, jsonObject)

def get_file_unique(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return file["content"]
    return ""

def get_file_info(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return file
    return {}

def enter_directory(folders):
    mainDir = folders[0]
    folders.pop(0)
    return mainDir

def get_content_from_path(folders, jsonObject):
    mainDir = enter_directory(folders)
    return recurse_dirs(folders, jsonObject[mainDir])

def is_unique_dir(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    for subDir in directory["directories"]:
        if subDir["name"] == name:
            return False
    return True

def file_is_unique(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return False
    return True

def space_available_file(path, content):
    jsonObject = read_from_json()
    return jsonObject["total_space"] >= jsonObject["used_space"] + len(content)

def space_available_existing_file(path, fileName, content):
    existing_file = get_file_info(path, fileName)
    jsonObject = read_from_json()
    return jsonObject["total_space"] >= jsonObject["used_space"] -  existing_file["size"]  + len(content)

def get_size_of_directory(directory):
    size = 0
    for file in directory["files"]:
        size += file["size"]
    return size

def recurse_size_of_directory(directory):
    if len(directory["directories"]) == 0:
        return get_size_of_directory(directory)
    else:
        size = 0
        for subDir in directory["directories"]:
            size += recurse_size_of_directory(subDir)
        size += get_size_of_directory(directory)
        return size

def delete_all_files_directory(directory):
    for file in directory["files"]:
        delete_data_virtual_disk(file["virtual_location"])
    return 

def recursive_rm_files_vdisk(directory):
    if len(directory["directories"]) == 0:
        return delete_all_files_directory(directory)
    else:
        for subDir in directory["directories"]:
            recursive_rm_files_vdisk(subDir)
        delete_all_files_directory(directory)
        return 

def mkdir(path, name):
    folders = path.split("/")
    if not name_is_valid(name):
        return False
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    determine_action(directory, name, 0, jsonObject)
    write_to_json(jsonObject)
    return True

def rm_dir(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    determine_action(directory, name, 1, jsonObject)
    write_to_json(jsonObject)
    return True

def mk_file(path, name, extension, content):
    folders = path.split("/")
    if not name_is_valid(name) or not name_is_valid(extension):
        return False
    
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    determine_action(directory, name, 2, jsonObject, content, extension)
    write_to_json(jsonObject)
    return True

def rm_file(path, name):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    determine_action(directory, name, 3, jsonObject)
    write_to_json(jsonObject)
    return True

def modify_file(path, name, content):
    folders = path.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    determine_action(directory, name, 4, jsonObject, content)
    write_to_json(jsonObject)
    return True

def recurse_dirs(folders, jsonObject):
    if len(folders) == 0:
        return jsonObject
    else:
        for i, directory in enumerate(jsonObject["directories"]):
            if directory["name"] == folders[0]:
                return recurse_dirs(folders[1:], directory)
        return jsonObject

def determine_action(jsonObject, name, status, jsonHome, content=None, extension=None):
    match status:
        # Crea un nuevo directorio
        case 0:
            size = delete_dir_by_name(jsonObject, name)
            addSpace(jsonHome, -size)
            create_directory_by_Nname(jsonObject, name)
        # Elimina un directorio
        case 1:
            size = delete_dir_by_name(jsonObject, name)
            addSpace(jsonHome, -size)
        # Crea un nuevo archivo
        case 2:
            size = delete_file_by_name(jsonObject, name)
            addSpace(jsonHome, -size)
            size = create_file_by_name(jsonObject, name, extension, content)
            addSpace(jsonHome, size)
        # Elimina un archivo
        case 3:
            size = delete_file_by_name(jsonObject, name)
            addSpace(jsonHome, -size)
        # Modifica el contenido de un archivo
        case 4:
            size = modify_file_by_name(jsonObject, name, content)
            addSpace(jsonHome, size)
    return

def delete_dir_by_name(jsonObject, name):
    for i, directory in enumerate(jsonObject["directories"]):
        if directory["name"] == name:
            jsonObject["directories"].pop(i)
            recursive_rm_files_vdisk(directory)
            return recurse_size_of_directory(directory)
    return 0

def create_directory_by_Nname(jsonObject, name):
    jsonObject["directories"].append({
        "name": name,
        "directories": [],
        "files": []
    })
    return 0

def delete_file_by_name(jsonObject, name):
    for i, file in enumerate(jsonObject["files"]):
        if file["name"] == name:
            jsonObject["files"].pop(i)
            delete_data_virtual_disk(file["virtual_location"])
            return file["size"]

    # aqui creo que se debe llamar al
    return 0

def create_file_by_name(jsonObject, name, extension, content):
    x = datetime.datetime.now()
    time = x.strftime("%m/%d/%Y, %H:%M:%S")
    jsonObject["files"].append({
        "name": name,
        "creation": time,
        "modification": time,
        "extension": extension,
        "size": len(content),
        "content": content,
        "virtual_location": insert_virtual_disk(content)
    })
    return len(content)

def modify_file_by_name(jsonObject, name, content):
    x = datetime.datetime.now()
    time = x.strftime("%m/%d/%Y, %H:%M:%S")
    for file in jsonObject["files"]:
        if file["name"] == name:
            sizeDif = len(content) - file["size"]
            file["size"] = len(content)
            file["content"] = content
            file["modification"] = time
            if("virtual_location" in file):
                delete_data_virtual_disk(file["virtual_location"])
                file["virtual_location"]= insert_virtual_disk(content)
            else:
                file["virtual_location"]= insert_virtual_disk(content)
            return sizeDif
    return 0

def addSpace(jsonHome, space):
    jsonHome["used_space"] += space
    return

def move_file(path, name, newPath, isCopy=False):
    folders = path.split("/")
    newFolders = newPath.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    newDirectory = get_content_from_path(newFolders, jsonObject)
    size = move_file_by_name(directory, name, newDirectory, isCopy)
    addSpace(jsonObject, size)
    write_to_json(jsonObject)
    return True

def move_directory(path, name, newPath, isCopy=False):
    folders = path.split("/")
    newFolders = newPath.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    newDirectory = get_content_from_path(newFolders, jsonObject)
    size = move_directory_by_name(directory, name, newDirectory, isCopy)
    addSpace(jsonObject, size)
    write_to_json(jsonObject)
    return True


def move_file_by_name(directory, name, newDirectory, isCopy):
    x = datetime.datetime.now()
    time = x.strftime("%m/%d/%Y, %H:%M:%S")
    for i, file in enumerate(directory["files"]):
        if file["name"] == name:
            sizeDif = delete_file_by_name(newDirectory, name)
            file["modification"] = time
            newDirectory["files"].append(file)
            if not isCopy:
                directory["files"].pop(i)
            else:
                sizeDif = file["size"] - sizeDif
            return sizeDif
    return 0






def move_directory_by_name(directory, name, newDirectory, isCopy):
    for i, subDir in enumerate(directory["directories"]):
        if subDir["name"] == name:
            sizeDif = delete_dir_by_name(newDirectory, name)
            newDirectory["directories"].append(subDir)
            if not isCopy:
                directory["directories"].pop(i)
            else:
                sizeDif = recurse_size_of_directory(subDir) - sizeDif
            return sizeDif
    return 0



def copy_all_files_directory(directory):
    for file in directory["files"]:
        copy = file
        copy["virtual_location"] = insert_virtual_disk(copy["content"])
    return 

def recursive_cpy_files_vdisk(directory):
    if len(directory["directories"]) == 0:
        return copy_all_files_directory(directory)
    else:
        for subDir in directory["directories"]:
            recursive_cpy_files_vdisk(subDir)
        copy_all_files_directory(directory)
        return 


def copy_directory_by_name(path, name, newPath):
    folders = path.split("/")
    newFolders = newPath.split("/")
    jsonObject = read_from_json()
    directory = get_content_from_path(folders, jsonObject)
    newDirectory = get_content_from_path(newFolders, jsonObject)
    for i, subDir in enumerate(directory["directories"]):
        if subDir["name"] == name:
            sizeDif = recurse_size_of_directory(subDir)
            if  (jsonObject["total_space"] - jsonObject["used_space"]- sizeDif ) >= 0:
                recursive_cpy_files_vdisk(subDir)
                newDirectory["directories"].append(subDir)
                addSpace(jsonObject, sizeDif)
                write_to_json(jsonObject)
                return True
            else:
                return False
    
    return False
    


    

