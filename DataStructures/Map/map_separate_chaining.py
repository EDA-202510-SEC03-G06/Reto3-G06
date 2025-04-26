import random
from DataStructures.Map.map_entry import new_map_entry, get_key, get_value, set_value
from DataStructures.List import array_list as al
from DataStructures.Map.map_functions import next_prime, hash_value

def new_map(num_elements, load_factor, prime=109345121):
    """Crea una nueva tabla hash con Separate Chaining."""
    capacity = next_prime(max(1, int(num_elements / load_factor)))  
    
    scale = random.randint(1, prime - 1)  
    shift = random.randint(0, prime - 1)  
    
    table = al.new_list()
    for _ in range(capacity):
        al.add_last(table, al.new_list())  
    
    return {
        'prime': prime,
        'capacity': capacity,
        'scale': scale,
        'shift': shift,
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0
    }

def get_entry(my_map, key):
    """Busca una entrada en la tabla hash por su clave y la retorna si existe."""
    index = hash_value(my_map, key)  
    bucket = al.get_element(my_map['table'], index)  
    for i in range(al.size(bucket)):  
        entry = al.get_element(bucket, i)
        if get_key(entry) == key:
            return entry 
    return None

def put(my_map, key, value):
    """Inserta o actualiza un valor en la tabla hash."""
    index = hash_value(my_map, key)
    bucket = al.get_element(my_map['table'], index)
    
    existing_entry = get_entry(my_map, key)  

    if existing_entry:
        set_value(existing_entry, value)
    else:
        new_entry = new_map_entry(key, value)
        al.add_last(bucket, new_entry)
        my_map['size'] += 1
        
        my_map['current_factor'] = my_map['size'] / my_map['capacity']
        if my_map['current_factor'] > my_map['limit_factor']:
            rehash(my_map)
    
    return my_map

def default_compare(key, element):
    """
    Función de comparación por defecto para comparar una llave con una entrada.

    :param key: Llave con la que se desea comparar.
    :param element: Entrada de la tabla de símbolos.
    :return: 0 si son iguales, 1 si key > entry_key, -1 si key < entry_key
    """
    entry_key = get_key(element)
    
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1

def contains(my_map, key):
    """
    Verifica si una llave se encuentra en la tabla de símbolos.

    :param my_map: Tabla de símbolos en la que se busca la llave.
    :param key: Llave que se desea verificar.
    :return: True si la llave está en la tabla, False en caso contrario.
    """
    index = hash_value(my_map, key)
    
    bucket = al.get_element(my_map['table'], index)
    
    for i in range(al.size(bucket)):
        entry = al.get_element(bucket, i)
        if default_compare(key, entry) == 0:
            return True
    
    return False

def remove(my_map, key):
    """
    Elimina una entrada de la tabla de símbolos asociada a una llave dada.

    :param my_map: Tabla de símbolos en la cual se desea eliminar una entrada.
    :param key: Llave de la entrada que se desea eliminar.
    :return: Tabla de símbolos con la entrada eliminada.
    """
    
    index = hash_value(my_map, key)

    
    bucket = al.get_element(my_map['table'], index)

    
    for i in range(al.size(bucket)):
        entry = al.get_element(bucket, i)
        if get_key(entry) == key:
            al.delete_element(bucket, i) 
            my_map['size'] -= 1  
            return my_map 

    return my_map  

def get(my_map, key):
    """
    Obtiene el valor asociado a una llave en la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener el valor asociado a una llave.
    :param key: Llave de la cual se desea obtener el valor asociado.
    :return: Valor asociado a la llave en la tabla de símbolos, o None si la llave no existe.
    """
    index = hash_value(my_map, key)
    bucket = al.get_element(my_map['table'], index)

    for i in range(al.size(bucket)):
        entry = al.get_element(bucket, i)
        if get_key(entry) == key:
            return get_value(entry) 

    return None 

def size(my_map):
    """
    Obtiene la cantidad de elementos en la tabla de símbolos.

    :param my_map: Tabla de símbolos de la cual se desea obtener la cantidad de elementos.
    :return: Cantidad de elementos en la tabla de símbolos.
    """
    return my_map['size']

def height(my_map):
    if my_map is None or my_map['table'] is None:
        return 0
    max_height = 0
    for i in range(al.size(my_map['table'])):
        bucket = al.get_element(my_map['table'], i)
        current_height = al.size(bucket)   
        if current_height > max_height:
            max_height = current_height
    return max_height

def is_empty(my_map):
    """
    Verifica si la tabla de símbolos se encuentra vacía.

    :param my_map: Tabla de símbolos de la cual se desea verificar si está vacía.
    :return: True si la tabla está vacía, False en caso contrario.
    """
    return my_map['size'] == 0

def key_set(my_map):
    """
    Obtiene la lista de llaves de la tabla de símbolos.
    """
    keys = al.new_list()  
    for i in range(al.size(my_map['table'])):  # Itera sobre los buckets
        bucket = al.get_element(my_map['table'], i)
        for j in range(al.size(bucket)):  # Itera sobre cada entrada en el bucket
            entry = al.get_element(bucket, j)
            al.add_last(keys, get_key(entry))
    
    return keys

def value_set(my_map):
    """
    Obtiene la lista de valores de la tabla de símbolos.
    """
    values = al.new_list()
    for i in range(al.size(my_map['table'])):
        bucket = al.get_element(my_map['table'], i)
        for j in range(al.size(bucket)):
            entry = al.get_element(bucket, j)
            al.add_last(values, get_value(entry))
    
    return values


def rehash(my_map):
    """Duplica la capacidad de la tabla hash y reorganiza los elementos."""
    old_table = my_map['table']
    new_capacity = my_map['capacity'] * 2 + 1  
    my_map['capacity'] = new_capacity
    my_map['size'] = 0  
    
    my_map['table'] = al.new_list()
    for _ in range(new_capacity):
        al.add_last(my_map['table'], al.new_list())  

    for i in range(al.size(old_table)):
        bucket = al.get_element(old_table, i)
        for j in range(al.size(bucket)):
            entry = al.get_element(bucket, j)
            put(my_map, get_key(entry), get_value(entry))  