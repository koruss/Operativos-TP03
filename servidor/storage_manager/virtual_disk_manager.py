# ━━━━-╮
# ╰┃ ┣▇━▇
#  ┃ ┃  ╰━▅╮
#  ╰┳╯ ╰━━┳╯F A S I L I T O
#   ╰╮ ┳━━╯ F A S I L I T O
#  ▕▔▋ ╰╮╭━╮F A S I L I T O
# ╱▔╲▋╰━┻┻╮╲╱▔▔▔╲
# ▏  ▔▔▔▔▔▔▔  O O┃
# ╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱
#  ▏╳▕▇▇▕ ▏╳▕▇▇▕
#  ╲▂╱╲▂╱ ╲▂╱



space_available = 0

def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

def create_virtual_disk(sectors, sectors_size):
    '''Crea la memoria virtual donde cada fila equivale a un sector, cada sector
    se inicializa con 0s '''
    with open('virtualDisk', "w", encoding='UTF-8') as f:
        for i in range(sectors):
            f.write("♣" * sectors_size)
            f.write("\n")
        f.close();
    space_available = sectors * sectors_size

def insert_virtual_disk(data):
    data_idx=0
    sector_idx=0
    char_num=0
    dict = {}
    matrix= []
    # guarda todas las lineas del file en un arreglo en memoria
    with open('virtualDisk', "r", encoding='UTF-8') as file:
        for line in file:
            matrix.append(line)
    file.close()
    # por cada linea del arreglo
    for sector in matrix:
        char_num = 0
        sector_list = Convert(sector)
        for char in sector:
            if data_idx < len(data):
                # si el char tiene ese caracter significa que esta vacio
                if char == '♣':
                    # se le asigna el caracter de la data a a la memoria            
                    sector_list[char_num] = data[data_idx]       
                    #str' object does not support item assignment se incrementa el contador de la data
                    data_idx=data_idx+1
                    # si en el diccionario ya existe el sector
                    if sector_idx in dict.keys():
                    # agrega la posicion del char en el sector al arreglo
                        list = dict[sector_idx]
                        list.append(char_num)
                    else:
                    # si no existe el sector lo anade y agrega 
                        dict[sector_idx] = [char_num]
            else:
                break                  
            char_num = char_num + 1
            # si ya acabamos el sector se mueve al siguiente
        matrix[sector_idx] = ''.join(sector_list)
        sector_idx=sector_idx+1
    with open('virtualDisk', "w", encoding='UTF-8') as file:
        for line in matrix:
            file.write(line)
    file.close()
    return dict


def delete_data_virtual_disk(dictionary):
    matrix= []
    list_of_keys = dictionary.keys()
    with open('virtualDisk', "r", encoding='UTF-8') as file:
        for line in file:
            matrix.append(Convert(line))
    file.close()
    for key in list_of_keys:
        places = dictionary[key]
        for place in places:
            matrix[key][place] = '♣'

    with open('virtualDisk', "w", encoding='UTF-8') as file:
        for line in matrix:
            file.write(''.join(line))
    file.close()

