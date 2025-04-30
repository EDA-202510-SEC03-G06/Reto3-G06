def new_map():
    """Crea un nuevo árbol rojo-negro vacío"""
    return {
        'root': None,  # Nodo raíz del árbol
        'type': 'RBT', # Tipo de estructura
        'size': 0      # Tamaño del árbol
    }

def is_red(node):
    """Determina si un nodo es rojo (los nodos None se consideran negros)"""
    if node is None:
        return False
    return node.get('color') == 'RED'

def size(node):
    """Retorna el tamaño de un subárbol"""
    return 0 if node is None else node.get('size', 0)

def rotate_left(h):
    """Rotación izquierda para balancear el árbol"""
    x = h['right']
    h['right'] = x['left']
    x['left'] = h
    x['color'] = h['color']
    h['color'] = 'RED'
    x['size'] = h['size']
    h['size'] = 1 + size(h['left']) + size(h['right'])
    return x

def rotate_right(h):
    """Rotación derecha para balancear el árbol"""
    x = h['left']
    h['left'] = x['right']
    x['right'] = h
    x['color'] = h['color']
    h['color'] = 'RED'
    x['size'] = h['size']
    h['size'] = 1 + size(h['left']) + size(h['right'])
    return x

def flip_colors(node):
    """Invierte los colores de un nodo y sus hijos"""
    node['color'] = 'RED' if node['color'] == 'BLACK' else 'BLACK'
    if node['left']:
        node['left']['color'] = 'RED' if node['left']['color'] == 'BLACK' else 'BLACK'
    if node['right']:
        node['right']['color'] = 'RED' if node['right']['color'] == 'BLACK' else 'BLACK'

def put(my_rbt, key, value):
    """Inserta un nuevo par clave-valor en el árbol"""
    if my_rbt is None:
        my_rbt = new_map()
    
    my_rbt['root'] = _put(my_rbt.get('root'), key, value)
    if my_rbt['root']:
        my_rbt['root']['color'] = 'BLACK'  # La raíz siempre es negra
    my_rbt['size'] = size(my_rbt['root'])
    return my_rbt

def _put(node, key, value):
    """Función auxiliar recursiva para inserción"""
    if node is None:
        return {
            'key': key,
            'value': value,
            'left': None,
            'right': None,
            'color': 'RED',  # Los nuevos nodos son rojos por defecto
            'size': 1
        }
    
    if key < node['key']:
        node['left'] = _put(node['left'], key, value)
    elif key > node['key']:
        node['right'] = _put(node['right'], key, value)
    else:
        node['value'] = value  # Actualiza el valor si la clave ya existe
    
    # Balancear el árbol
    if is_red(node['right']) and not is_red(node['left']):
        node = rotate_left(node)
    if is_red(node['left']) and is_red(node['left']['left']):
        node = rotate_right(node)
    if is_red(node['left']) and is_red(node['right']):
        flip_colors(node)
    
    node['size'] = 1 + size(node['left']) + size(node['right'])
    return node

def get(my_rbt, key):
    """Obtiene el valor asociado a una clave"""
    node = get_node(my_rbt.get('root'), key)
    return node['value'] if node else None

def get_node(node, key):
    """Busca un nodo por su clave"""
    if node is None:
        return None
    
    if key < node['key']:
        return get_node(node['left'], key)
    elif key > node['key']:
        return get_node(node['right'], key)
    else:
        return node

def contains(my_rbt, key):
    """Verifica si una clave existe en el árbol"""
    return get(my_rbt, key) is not None

def is_empty(my_rbt):
    """Determina si el árbol está vacío"""
    if my_rbt is None:
        return True
    if my_rbt.get('root') is None:
        return True
    # Verificación adicional para casos donde size no está actualizado
    if my_rbt.get('size', 0) == 0 and _count_nodes(my_rbt['root']) == 0:
        return True
    return False

def _count_nodes(node):
    """Cuenta los nodos en el árbol (para verificación de consistencia)"""
    if node is None:
        return 0
    return 1 + _count_nodes(node.get('left')) + _count_nodes(node.get('right'))

def key_set(my_rbt):
    """Retorna una estructura de lista enlazada con todas las claves"""
    class LinkedListNode:
        def _init_(self, element, next_node=None):
            self.element = element
            self.next = next_node

    keys = []
    def in_order_traversal(node):
        if node is None:
            return
        in_order_traversal(node.get('left'))
        keys.append(node['key'])
        in_order_traversal(node.get('right'))
    
    in_order_traversal(my_rbt.get('root'))
    
    if not keys:
        return {'first': None}
    
    head = LinkedListNode(keys[-1])
    for key in reversed(keys[:-1]):
        head = LinkedListNode(key, head)
    
    return {'first': head}

def value_set(my_rbt):
    """Retorna una estructura de lista enlazada con todos los valores"""
    class LinkedListNode:
        def _init_(self, element, next_node=None):
            self.element = element
            self.next = next_node

    values = []
    def in_order_traversal(node):
        if node is None:
            return
        in_order_traversal(node.get('left'))
        values.append(node['value'])
        in_order_traversal(node.get('right'))
    
    in_order_traversal(my_rbt.get('root'))
    
    if not values:
        return {'first': None}
    
    head = LinkedListNode(values[-1])
    for value in reversed(values[:-1]):
        head = LinkedListNode(value, head)
    
    return {'first': head}

def _in_order_traversal(node, result, attr):
    """Recorrido in-order para recolectar claves o valores"""
    if node is None:
        return
    _in_order_traversal(node.get('left'), result, attr)
    result.append(node[attr])
    _in_order_traversal(node.get('right'), result, attr)

def get_min_node(node):
    """Encuentra el nodo con la clave mínima"""
    if node is None:
        return None
    while node.get('left') is not None:
        node = node['left']
    return node

def get_min(my_rbt):
    """Obtiene la clave mínima del árbol"""
    min_node = get_min_node(my_rbt.get('root'))
    return min_node['key'] if min_node else None

def get_max_node(node):
    """Encuentra el nodo con la clave máxima"""
    if node is None:
        return None
    while node.get('right') is not None:
        node = node['right']
    return node

def get_max(my_rbt):
    """Obtiene la clave máxima del árbol"""
    max_node = get_max_node(my_rbt.get('root'))
    return max_node['key'] if max_node else None

def move_red_left(node):
    """Mueve un nodo rojo a la izquierda para balancear"""
    flip_colors(node)
    if node.get('right') and is_red(node['right']['left']):
        node['right'] = rotate_right(node['right'])
        node = rotate_left(node)
        flip_colors(node)
    return node

def move_red_right(node):
    """Mueve un nodo rojo a la derecha para balancear"""
    flip_colors(node)
    if node.get('left') and is_red(node['left']['left']):
        node = rotate_right(node)
        flip_colors(node)
    return node

def balance(node):
    """Balancea el árbol después de operaciones"""
    if node is None:
        return None
    
    if is_red(node.get('right')) and not is_red(node.get('left')):
        node = rotate_left(node)
    if is_red(node.get('left')) and is_red(node['left']['left']):
        node = rotate_right(node)
    if is_red(node.get('left')) and is_red(node.get('right')):
        flip_colors(node)
    
    node['size'] = 1 + size(node.get('left')) + size(node.get('right'))
    return node

def delete_min(my_rbt):
    """Elimina el nodo con la clave mínima"""
    if is_empty(my_rbt):
        return my_rbt
    
    root = my_rbt.get('root')
    if root and not is_red(root.get('left')) and not is_red(root.get('right')):
        root['color'] = 'RED'
    
    my_rbt['root'] = _delete_min(root) if root else None
    if not is_empty(my_rbt) and my_rbt['root']:
        my_rbt['root']['color'] = 'BLACK'
    my_rbt['size'] = size(my_rbt.get('root'))
    return my_rbt

def _delete_min(node):
    """Función auxiliar para eliminar el mínimo"""
    if node.get('left') is None:
        return None
    
    if not is_red(node.get('left')) and not is_red(node['left']['left']):
        node = move_red_left(node)
    
    node['left'] = _delete_min(node['left'])
    return balance(node)

def delete_max(my_rbt):
    """Elimina el nodo con la clave máxima"""
    if is_empty(my_rbt):
        return my_rbt
    
    root = my_rbt.get('root')
    if root and not is_red(root.get('left')) and not is_red(root.get('right')):
        root['color'] = 'RED'
    
    my_rbt['root'] = _delete_max(root) if root else None
    if not is_empty(my_rbt) and my_rbt['root']:
        my_rbt['root']['color'] = 'BLACK'
    my_rbt['size'] = size(my_rbt.get('root'))
    return my_rbt

def _delete_max(node):
    """Función auxiliar para eliminar el máximo"""
    if is_red(node.get('left')):
        node = rotate_right(node)
    
    if node.get('right') is None:
        return None
    
    if not is_red(node.get('right')) and not is_red(node['right']['left']):
        node = move_red_right(node)
    
    node['right'] = _delete_max(node['right'])
    return balance(node)

def floor(my_rbt, key):
    """Encuentra la clave más grande menor o igual a la clave dada"""
    node = _floor(my_rbt.get('root'), key)
    return node['key'] if node else None

def _floor(node, key):
    """Función auxiliar para floor"""
    if node is None:
        return None
    
    if key == node['key']:
        return node
    
    if key < node['key']:
        return _floor(node.get('left'), key)
    
    t = _floor(node.get('right'), key)
    return t if t is not None else node

def ceiling(my_rbt, key):
    """Encuentra la clave más pequeña mayor o igual a la clave dada"""
    node = _ceiling(my_rbt.get('root'), key)
    return node['key'] if node else None

def _ceiling(node, key):
    """Función auxiliar para ceiling"""
    if node is None:
        return None
    
    if key == node['key']:
        return node
    
    if key > node['key']:
        return _ceiling(node.get('right'), key)
    
    t = _ceiling(node.get('left'), key)
    return t if t is not None else node

def keys(my_rbt, key_lo, key_hi):
    """Retorna todas las claves en el rango [key_lo, key_hi]"""
    keys_list = []
    _keys_range(my_rbt.get('root'), keys_list, key_lo, key_hi)
    return keys_list

def left_key(my_rbt):
    if my_rbt is None or my_rbt.get('root') is None:
        return None
    node = my_rbt['root']
    while node.get('left') is not None:
        node = node['left']
    return node['key']

def right_key(my_rbt):
    if my_rbt is None or my_rbt.get('root') is None:
        return None
    node = my_rbt['root']
    while node.get('right') is not None:
        node = node['right']
    return node['key']


def _keys_range(node, keys_list, key_lo, key_hi):
    """Función auxiliar para keys"""
    if node is None:
        return
    
    if key_lo < node['key']:
        _keys_range(node.get('left'), keys_list, key_lo, key_hi)
    
    if key_lo <= node['key'] <= key_hi:
        keys_list.append(node['key'])
    
    if key_hi > node['key']:
        _keys_range(node.get('right'), keys_list, key_lo, key_hi)

def values(my_rbt, key_lo, key_hi):
    """Retorna todos los valores en el rango [key_lo, key_hi]"""
    values_list = []
    _values_range(my_rbt.get('root'), values_list, key_lo, key_hi)
    return values_list

def _values_range(node, values_list, key_lo, key_hi):
    """Función auxiliar para values"""
    if node is None:
        return
    
    if key_lo < node['key']:
        _values_range(node.get('left'), values_list, key_lo, key_hi)
    
    if key_lo <= node['key'] <= key_hi:
        values_list.append(node['value'])
    
    if key_hi > node['key']:
        _values_range(node.get('right'), values_list, key_lo, key_hi)

def height(my_rbt):
    """Retorna la altura del árbol"""
    return _height(my_rbt.get('root'))

def _height(node):
    """Función auxiliar para calcular altura"""
    if node is None:
        return -1
    return 1 + max(_height(node.get('left')), _height(node.get('right')))


def get_sorted(my_rbt):
    result = []
    def in_order_traversal(node):
        if node is None:
            return
        in_order_traversal(node.get('left'))
        result.append(node['value'])
        in_order_traversal(node.get('right'))
    
    in_order_traversal(my_rbt.get('root'))
    return result