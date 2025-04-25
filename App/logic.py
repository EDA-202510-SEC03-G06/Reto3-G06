import csv
import sys
from datetime import datetime
from collections import defaultdict

# Configuración inicial para manejar archivos grandes
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

def new_logic():
    """
    Inicializa las estructuras de datos para almacenar la información de crímenes.
    Returns:
        dict: Diccionario con estructuras vacías para organizar los datos
    """
    return {
        'crimes_by_id': {},                      # Mapa por ID único del crimen
        'crimes_by_date': defaultdict(list),     # Crimenes agrupados por fecha
        'crimes_by_area': defaultdict(list),     # Crimenes agrupados por área policial
        'coordinates': [],                       # Lista de tuplas (latitud, longitud)
        'total_crimes': 0                        # Contador total de crímenes
    }

def load_data(catalog, filename):
    """
    Carga los datos del archivo CSV en las estructuras del catálogo.
    Args:
        catalog (dict): Catálogo inicializado con new_logic()
        filename (str): Ruta al archivo CSV con los datos
    """
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Procesamiento directo de los datos
            crime_id = row['DR_NO']
            date_str = row['DATE OCC']
            crime_date = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p').date()
            area = row['AREA']
            lat = float(row['LAT']) if row['LAT'] else 0.0
            lon = float(row['LON']) if row['LON'] else 0.0
            
            # Almacenamiento en estructuras
            catalog['crimes_by_id'][crime_id] = row
            catalog['crimes_by_date'][crime_date].append(row)
            catalog['crimes_by_area'][area].append(row)
            
            if lat != 0.0 and lon != 0.0:
                catalog['coordinates'].append((lat, lon))
                
            catalog['total_crimes'] += 1

def get_data(catalog, crime_id):
    """
    Recupera un crimen específico por su ID.
    Args:
        catalog (dict): Catálogo con los datos cargados
        crime_id (str): ID del crimen a buscar
    Returns:
        dict or None: Datos del crimen si existe, None en caso contrario
    """
    return catalog['crimes_by_id'].get(crime_id)

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
