
import csv
import sys
import time
import os
from datetime import datetime

# Configuración inicial para manejar archivos grandes
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

def new_logic():
    """Crea estructuras de datos vacías"""
    return {
        'crimes_by_id': {},
        'crimes_by_date': {},
        'crimes_by_area': {},
        'coordinates': [],
        'total_crimes': 0
    }

def load_data(catalog, filename):
    """Carga datos desde archivo CSV con manejo de errores"""
    # Validación básica de entrada
    if not isinstance(filename, str) or not filename.strip():
        print("Error: Nombre de archivo inválido")
        return None
    
    filename = filename.strip()
    if not filename.lower().endswith('.csv'):
        filename += '.csv'
    
    # Buscar archivo en múltiples ubicaciones
    search_paths = [
        filename,
        os.path.join('Data', filename),
        os.path.join('../Data', filename)
    ]
    
    found_path = None
    for path in search_paths:
        if os.path.exists(path):
            found_path = path
            break
    
    if not found_path:
        print("Error: Archivo no encontrado en las siguientes ubicaciones:")
        for path in search_paths:
            print(f"- {os.path.abspath(path)}")
        
        # Mostrar archivos CSV disponibles
        print("\nArchivos CSV disponibles:")
        for root, _, files in os.walk('.'):
            for file in files:
                if file.lower().endswith('.csv'):
                    print(f"- {os.path.join(root, file)}")
        return None
    
    print(f"\nCargando datos desde: {found_path}")
    
    processed = 0
    skipped = 0
    
    try:
        with open(found_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    # Validación de campos obligatorios
                    required_fields = ['DR_NO', 'DATE OCC', 'AREA', 'LAT', 'LON']
                    if not all(field in row for field in required_fields):
                        skipped += 1
                        continue
                    
                    # Parseo de fecha
                    date_str = row['DATE OCC'].strip()
                    crime_date = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p').date()
                    
                    # Parseo de coordenadas
                    lat_str = row['LAT'].strip()
                    lon_str = row['LON'].strip()
                    lat = float(lat_str) if lat_str else 0.0
                    lon = float(lon_str) if lon_str else 0.0
                    
                    # Almacenamiento
                    crime_id = row['DR_NO']
                    catalog['crimes_by_id'][crime_id] = row
                    
                    if crime_date not in catalog['crimes_by_date']:
                        catalog['crimes_by_date'][crime_date] = []
                    catalog['crimes_by_date'][crime_date].append(row)
                    
                    area = row['AREA']
                    if area not in catalog['crimes_by_area']:
                        catalog['crimes_by_area'][area] = []
                    catalog['crimes_by_area'][area].append(row)
                    
                    if lat != 0.0 and lon != 0.0:
                        catalog['coordinates'].append((lat, lon))
                    
                    catalog['total_crimes'] += 1
                    processed += 1
                
                except ValueError:
                    skipped += 1
                    continue
        
        print(f"\nResumen de carga:")
        print(f"- Registros procesados: {processed}")
        print(f"- Registros omitidos: {skipped}")
        print(f"- Total en catálogo: {catalog['total_crimes']}")
        
        return catalog
    
    except PermissionError:
        print("Error: No tiene permisos para leer el archivo")
        return None
    except csv.Error:
        print("Error: El archivo CSV está mal formado")
        return None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None

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
