from storage_manager.json_manager import *
import datetime

def get_directory(path):
    folders = path.split("/")
    jsonObject = read_from_json(folders[0])
    return get_content_from_path(folders, jsonObject)

def get_file(path, name):
    folders = path.split("/")
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return file["content"]
    return ""

def get_file_info(path, name):
    folders = path.split("/")
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return file
    return {}

# def isHomeDir(folders):
#     if len(folders) <= 1:
#         return True
#     return False

def enter_directory(folders):
    folders.pop(0)
    mainDir = folders[0]
    folders.pop(0)
    return mainDir

def get_content_from_path(folders, jsonObject):
    mainDir = enter_directory(folders)
    return recurse_dirs(folders, jsonObject[mainDir])

def is_unique_dir(path, name):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return True
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    for subDir in directory["directories"]:
        if subDir["name"] == name:
            return False
    return True

def file_is_unique(path, name):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return True
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    for file in directory["files"]:
        if file["name"] == name:
            return False
    return True

def space_available_file(path, content):
    username = path.split("/")[0]
    jsonObject = read_from_json(username)
    return jsonObject["size"] >= jsonObject["used"] + len(content)

# def spaceAvailableShareFile(targetUser, sharingPath, sharingName):
#     jsonObject = read_from_json(targetUser)
#     size = getFileProperties(sharingPath, sharingName)["size"]
#     return jsonObject["size"] >= jsonObject["used"] + size

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

# def spaceAvailableShareDir(targetUser, sharingPath, sharingName):
#     jsonObject = read_from_json(targetUser)
#     folders = sharingPath.split("/")
#     jsonSharingObject = read_from_json(folders[0])
#     directory = getContentFromPath(folders + [sharingName], jsonSharingObject)
#     size = recurseSizeOfDir(directory)
#     return jsonObject["size"] >= jsonObject["used"] + size

def mkdir(path, name):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return False
    if not name_is_valid(name):
        return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    do_some_option(directory, name, 0, jsonObject)
    write_to_json(jsonObject)
    return True

def rm_dir(path, name):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    do_some_option(directory, name, 1, jsonObject)
    write_to_json(jsonObject)
    return True

def mk_file(path, name, extension, content):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return False
    if not nameIsValid(name) or not nameIsValid(extension):
        return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    do_some_option(directory, name, 2, jsonObject, content, extension)
    write_to_json(jsonObject)
    return True

def rm_file(path, name):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    do_some_option(directory, name, 3, jsonObject)
    write_to_json(jsonObject)
    return True

def modify_file(path, name, content):
    folders = path.split("/")
    # if isHomeDir(folders):
    #     return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    do_some_option(directory, name, 4, jsonObject, content)
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

def do_some_option(jsonObject, name, status, jsonHome, content=None, extension=None):
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
            return file["size"]
    # aqui creo que se debe llamar al
    return 0

def create_file_by_name(jsonObject, name, extension, content):
    jsonObject["files"].append({
        "name": name,
        "extension": extension,
        "size": len(content),
        "content": content
    })
    return len(content)

def modify_file_by_name(jsonObject, name, content):
    for file in jsonObject["files"]:
        if file["name"] == name:
            sizeDif = len(content) - file["size"]
            file["size"] = len(content)
            file["content"] = content
            return sizeDif
    return 0

def addSpace(jsonHome, space):
    jsonHome["used"] += space
    return

def move_file(path, name, newPath, isCopy=False):
    folders = path.split("/")
    newFolders = newPath.split("/")
    # if isHomeDir(folders) or isHomeDir(newFolders):
    #     return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    newDirectory = get_content_from_path(newFolders, jsonObject)
    return True

def move_directory(path, name, newPath, isCopy=False):
    folders = path.split("/")
    newFolders = newPath.split("/")
    # if isHomeDir(folders) or isHomeDir(newFolders):
    #     return False
    jsonObject = read_from_json(folders[0])
    directory = get_content_from_path(folders, jsonObject)
    newDirectory = get_content_from_path(newFolders, jsonObject)
    size = move_directory_by_name(directory, name, newDirectory, isCopy)
    addSpace(jsonObject, size)
    write_to_json(jsonObject)
    return True

# def shareFile(path, name, newUser):
#     folders = path.split("/")
#     if isHomeDir(folders):
#         return False
#     jsonObject = read_from_json(folders[0])
#     jsonNewUser = read_from_json(newUser)
#     directory = getContentFromPath(folders, jsonObject)
#     newDirectory = jsonNewUser["shared"]
#     size = move_file_by_name(directory, name, newDirectory, True)
#     addSpace(jsonNewUser, size)
#     write_to_json(jsonObject)
#     write_to_json(jsonNewUser)
#     return True

# def shareDir(path, name, newUser):
#     folders = path.split("/")
#     if isHomeDir(folders):
#         return False
#     jsonObject = read_from_json(folders[0])
#     jsonNewUser = read_from_json(newUser)
#     directory = getContentFromPath(folders, jsonObject)
#     newDirectory = jsonNewUser["shared"]
#     size = move_directory_by_name(directory, name, newDirectory, True)
#     addSpace(jsonNewUser, size)
#     write_to_json(jsonObject)
#     write_to_json(jsonNewUser)
#     return True

def move_file_by_name(directory, name, newDirectory, isCopy):
    for i, file in enumerate(directory["files"]):
        if file["name"] == name:
            sizeDif = delete_file_by_name(newDirectory, name)
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
