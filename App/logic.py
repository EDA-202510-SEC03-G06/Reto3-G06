
import csv
import sys
import time
import os
from datetime import datetime
from DataStructures.List import array_list as lt
from DataStructures.Tree import red_black_tree as rbt
import math

# Configuración inicial para manejar archivos grandes
csv.field_size_limit(2147483647)
sys.setrecursionlimit(10000)

def new_logic():
    """Crea estructuras de datos vacías"""
    return {
        "crimes_by_id": {},
        "crimes_by_date": {},
        "crimes_by_area": {},
        "coordinates": [],
        "total_crimes": 0
    }

def load_data(catalog, filename):
    """Carga datos desde archivo CSV con manejo de errores"""
    start_time = get_time()
    procesado = 0
    saltado = 0
    primeros_reportes = []
    ultimos_reportes = []
    # hago una validación básica de entrada
    if not isinstance(filename, str) or not filename.strip():
        print("Error: Nombre de archivo inválido")
        return None
    
    filename = filename.strip()
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    
    # Buscar archivo
    archivos_busq = [
        filename,
        os.path.join("Data", filename)
    ]
    
    archivos_enc = None
    for path in archivos_busq:
        if os.path.exists(path):
            archivos_enc = path
    
    if not archivos_enc: #mido el caso en el que no se encuentre el archivo
        return None
    
    
    with open(archivos_enc, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
            
        for valor in reader:
            try:
                    # valido los campos obligatorios
                requerimientos_v = ["DR_NO", "DATE OCC", "AREA", "LAT", "LON", "Date Rptd", "AREA NAME", "Crm Cd"]
                if not all(field in valor for field in requerimientos_v): #la funcion all() devuelve True si todos los elementos de la lista son True, fuente: https://micro.recursospython.com/recursos/la-funcion-all.html
                        saltado += 1
                        continue
                    
                    # fechas
                dato_str = valor["DATE OCC"].strip()
                date_rptd = valor["Date Rptd"].strip()
                
                crime_date = datetime.strptime(dato_str, "%m/%d/%Y %I:%M:%S %p").date()
                report_date = datetime.strptime(date_rptd, "%m/%d/%Y %I:%M:%S %p").date()
                    # coordenadas
                lat_str = valor["LAT"].strip()
                lon_str = valor["LON"].strip()
                lat = float(lat_str) if lat_str else 0
                lon = float(lon_str) if lon_str else 0
                    
                crime_id = valor["DR_NO"]
                catalog["crimes_by_id"][crime_id] = valor
                    
                if crime_date not in catalog["crimes_by_date"]:
                        catalog["crimes_by_date"][crime_date] = []
                catalog["crimes_by_date"][crime_date].append(valor)
                    
                area = valor["AREA"]
                if area not in catalog["crimes_by_area"]:
                    catalog["crimes_by_area"][area] = []
                catalog["crimes_by_area"][area].append(valor)
                    
                if lat != 0 and lon != 0:
                    catalog["coordinates"].append((lat, lon))
                    
                reporte= {
                    "DR_NO": valor.get("DR_NO", "Unknown"),
                    "Date Rptd": valor.get("Date Rptd", "Unknown"),
                    "DATE OCC": valor.get("DATE OCC", "Unknown"),
                    "AREA NAME": valor.get("AREA NAME", "Unknown"),
                    "Crm Cd": valor.get("Crm Cd", "Unknown")
                }
                
                if len(primeros_reportes) < 5:
                    primeros_reportes.append(reporte)
                
                ultimos_reportes.append(reporte)
                if len(primeros_reportes) >= 5:
                    ultimos_reportes.pop(0)
                        
                    
                catalog["total_crimes"] += 1
                procesado += 1
                
            except ValueError:
                saltado += 1
                continue
        end_time = get_time()
        elapsed_time = delta_time(start_time, end_time)
        
        print(f"\nResumen de carga:")
        print(f"- Registros procesados: {procesado}")
        print(f"- Registros omitidos: {saltado}")
        print(f"- Total en catálogo: {catalog["total_crimes"]}")
        print(f"- Tiempo de ejecución: {elapsed_time:.4f} ms")
        
        if procesado > 0:
            print(f"\nPrimeros 5 reportes:")
            for primero in primeros_reportes:
                print(f"DR_NO: {primero["DR_NO"]}")
                print(f"Date Rptd: {primero["Date Rptd"]}")
                print(f"DATE OCC: {primero["DATE OCC"]}")
                print(f"AREA NAME: {primero["AREA NAME"]}")
                print(f"Crm Cd: {primero["Crm Cd"]}")
                print("-" * 80)
                
        
            if procesado > 5:
                print("\nÚltimos 5 reportes:")
                ultimos_mostrar = ultimos_reportes[-5:] if len(ultimos_reportes) >= 5 else ultimos_reportes
                for i, reporte in enumerate(ultimos_mostrar, max(1, procesado - 4)):
                    print(f"\nReporte #{i}:")
                    print(f"DR_NO: {reporte["DR_NO"]}")
                    print(f"Fecha Reportado: {reporte["Date Rptd"]}")
                    print(f"Fecha Ocurrencia: {reporte["DATE OCC"]}")
                    print(f"Área: {reporte["AREA NAME"]}")
                    print(f"Código Crimen: {reporte["Crm Cd"]}")
                    print("-" * 60)
        print("\n" + "="*60)
        
        return catalog

def get_data(catalog, crime_id):
    """
    Recupera un crimen específico por su ID.
    Args:
        catalog (dict): Catálogo con los datos cargados
        crime_id (str): ID del crimen a buscar
    Returns:
        dict or None: Datos del crimen si existe, None en caso contrario
    """
    return catalog["crimes_by_id"].get(crime_id)

def req_1(catalog, dato_inicial_str, dato_final_str):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    result = []
    start_state = datetime.strptime(dato_inicial_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(dato_final_str, "%m/%d/%Y").date()
    
    # recorro todas las fechas y filtro por rango de fechas
    for crime in catalog["crimes_by_date"]:
        if start_state <= crime <= end_date:
            for datos_crime in catalog["crimes_by_date"][crime]:
                crime_date = datetime.strptime(datos_crime["DATE OCC"], "%m/%d/%Y %I:%M:%S %p")
                
                # creo un diccionario con la informacion de la crimen
                crime_info = {
                    "id": datos_crime["DR_NO"],
                    "date": crime_date.strftime("%Y-%m-%d"),
                    "time": crime_date.strftime("%H-%M-%S"),
                    "area": datos_crime.get("AREA NAME", "Desconocida"),
                    "codigo": datos_crime.get("Crm Cd", "N/A"),
                    "direccion": datos_crime.get("LOCATION", "Sin dirección"),
                    #agrego los datos temporales necesarios para ordenar el resultado
                    "sort_date": crime_date,
                    "codigo_de_area": int(datos_crime["AREA"]) if datos_crime["AREA"].isdigit() else 0
                }
                result.append(crime_info)
    # ordeno el resultado
    result.sort(key=lambda x: (-x["sort_date"].timestamp(), x["codigo_de_area"])) #con timestamp almaceno la  informacion de la fecha y codigo de area fuente https://skiller.education/timestamp/#:~:text=El%20tipo%20de%20dato%20TIMESTAMP%20es%20utilizado%20para%20almacenar%20información,en%20que%20ocurrió%20un%20evento.
    #elimino los campos temporales que uso para ordenar el resultado
    for crimen in result:
        del crimen["sort_date"]
        del crimen["codigo_de_area"]
    
    elapsed_time = delta_time(start_time, get_time())
    return {"result": result, "time": elapsed_time}
def req_2(catalog, dato_inicial_str, dato_final_str):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    result = []
    start_time = get_time()
    start_state = datetime.strptime(dato_inicial_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(dato_final_str, "%m/%d/%Y").date()
    
    for crime in catalog["crimes_by_date"]:
        if start_state <= crime <= end_date:
            for datos_crime in catalog["crimes_by_date"][crime]:
                #filtro de crimenes
                if (datos_crime.get("Part 1-2", " ").strip() == "1" and datos_crime.get("Status"," ").upper() == "AA"):
                    crime_date = datetime.strptime(datos_crime["DATE OCC"], "%m/%d/%Y %I:%M:%S %p")

                    # creo un diccionario con la informacion de la crimen
                    crime_info = {
                        "id": datos_crime["DR_NO"],
                        "date": crime_date.strftime("%Y-%m-%d"),
                        "time": crime_date.strftime("%H-%M-%S"),
                        "area": datos_crime.get("AREA NAME", "desconocida"),
                        "subarea": datos_crime.get("Rpt Dist No", "N/A"),
                        "gravedad": "Part 1-2",
                        "codigo":datos_crime.get("Crm Cd", "N/A"),
                        "estado":datos_crime.get("Status Desc", "desconocido"),
                        #agrego los datos temporales necesarios para ordenar el resultado
                        "sort_date": crime_date,
                        "codigo_de_area": int(datos_crime["AREA"]) if datos_crime["AREA"].isdigit() else 0
                    }
                    result.append(crime_info)
                
    result.sort(key=lambda x: (-x["sort_date"].timestamp(), x["codigo_de_area"]))
    for crimen in result:
        del crimen["sort_date"]
        del crimen["codigo_de_area"]
    
    elapsed_time = delta_time(start_time, get_time())
    return (len(result), result, elapsed_time)

def req_3(catalog, num, nomb_area):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    if not nomb_area or not isinstance(nomb_area, str):
        return (0, [])

    area_code = None
    filtro_area = str(nomb_area).strip().lower() if nomb_area else ""
    area_en = False
    
    for code, crimes in catalog["crimes_by_area"].items():
        if not area_en and crimes and isinstance(crimes[0], dict):
            area_name = crimes[0].get("AREA NAME")
            if area_name and str(area_name).strip().lower() == filtro_area:
                area_code = code
                area_en = True
    
    if area_code is None:
        return (0, [])

    crimenes_procesados = []
    for crime in catalog['crimes_by_area'][area_code]:
        if not isinstance(crime, dict):
            continue
        #reviso que esten todos los campos requeridos sean validos  
        requerimientos_v = {
            "DATE OCC": lambda x: bool(x),
            "TIME OCC": lambda x: str(x).isdigit(),
            "DR_NO": lambda x: bool(x),
            "AREA NAME": lambda x: bool(x),
            "Rpt Dist No": lambda x: True,
            "Part 1-2": lambda x: x in ['1', '2'],
            "Crm Cd": lambda x: bool(x),
            "Status Desc": lambda x: bool(x),
            "LOCATION": lambda x: bool(x)
        }

        valid = True
        for valor, validador in requerimientos_v.items():
            if valor not in crime or not validador(crime[valor]):
                valid = False
                continue # saltar al siguiente elemento, no es break jsjasjajs fuente: https://ellibrodepython.com/continue-python
        
        if not valid:
            continue

        dato_str = crime["DATE OCC"].split()[0] if "DATE OCC" in crime else ""
        dato_parts = dato_str.split('/') if dato_str else []
        
        if len(dato_parts) == 3:
            try:
                mes, dia, anio = map(int, dato_parts)
                time_occ = str(crime["TIME OCC"]).zfill(4)
                
                crimenes_procesados.append({
                    'crime': crime,
                    'sort_key': (anio, mes, dia, int(time_occ))
                })
            except (ValueError, TypeError):
                continue
    
    total_crimes = len(crimenes_procesados)
    if total_crimes == 0:
        return (0, [])

    crime_org = sorted(crimenes_procesados, key=lambda x: x['sort_key'], reverse=True)
    results = []
    for crime_data in crime_org[:num]:
        crime = crime_data['crime']

        time_str = str(crime.get("TIME OCC", "0000")).zfill(4)
        tiempo_form = f"{time_str[:2]}:{time_str[2:]}"
        
        results.append({
            'id': crime.get("DR_NO", "N/A"),
            'dato': crime.get("DATE OCC", "N/A").split()[0],
            'tiempo': tiempo_form,
            'area': crime.get("AREA NAME", "N/A"),
            'subarea': str(crime.get("Rpt Dist No", "N/A")),
            'gravedad': 'Part ' + str(crime.get("Part 1-2", "?")),
            'codigo': crime.get("Crm Cd", "N/A"),
            'estado': crime.get("Status Desc", "N/A"),
            'direccion': str(crime.get("LOCATION", "N/A")).strip()
        })
    end_time = get_time()
    return (total_crimes, results, delta_time(start_time, end_time))
        
        
def req_4(catalog, tipo_crimen, num, edad_final):
    """
    Retorna el resultado del requerimiento 4
    """
    filtro = []
    for crime in catalog["crimes_by_id"].values():
        if "Vict Age" in crime and isinstance(crime["Vict Age"], str) and crime["Vict Age"].isdigit():
            edad = int(crime["Vict Age"])
            if 0 <= edad <= edad_final:
                if tipo_crimen.upper() in crime.get("Crm Cd Desc", "").upper():
                    gravedad = 0 if crime.get("Part 1-2", "") == "1" else 1
                    sort_key = (gravedad, -edad, crime.get("DATE OCC", ""))
                    filtro.append({"sort_key": sort_key, "crime_data": crime})
    if lt.size(filtro) > 0:
        lt.quickSort(filtro, 0, len(filtro) - 1, lambda crime1, crime2: -1 if crime1["sort_key"] < crime2["sort_key"] else 1)
        total_crimes = lt.size(filtro)
        result_crimes = lt.new_list()
        minimo = min(num, total_crimes)
        for i in range(1, minimo + 1):
            crime_total= lt.get_element(filtro, i)
            crime = crime_total["crime_data"]
            gravedad_text = "Part 1" if crime.get("Part 1-2", "") == "1" else "Part 2"
            crime_info = {
                "report_id": crime.get("DR_NO", "N/A"),
                "date": crime.get("DATE OCC", "N/A"),
                "time": crime.get("TIME OCC", "N/A"),
                "area": crime.get("AREA NAME", "N/A"),
                "subarea": crime.get("Rpt Dist No", "N/A"),
                "severity": gravedad_text,
                "crime_code": crime.get("Crm Cd", "N/A"),
                "victim_age": crime.get("Vict Age", "N/A"),
                "case_status": crime.get("Status Desc", "N/A"),
                "address": crime.get("LOCATION", "N/A")
            }
            lt.add_last(result_crimes, crime_info)

        return total_crimes, result_crimes
    else:
        return 0, lt.new_list()

def req_5(catalog, N, fecha_inicial, fecha_final):
    #Intente usar array_list con quicksort pero no funciono
    if 'data' not in catalog or N <= 0:
        return []
    areas_info = {}
    for crimen in catalog['data']:
        if not all(key in crimen for key in ['DATE OCC','AREA','AREA NAME','Status Desc']):
            continue
        fecha_crimen = crimen['DATE OCC']
        area_id = str(crimen['AREA'])
        area_nombre = crimen['AREA NAME']
        estado = crimen['Status Desc'].upper()
        if (fecha_inicial <= fecha_crimen <= fecha_final) and 'CLEARED' not in estado:
            if area_id in areas_info:
                areas_info[area_id]['cantidad'] += 1
                if fecha_crimen < areas_info[area_id]['primera_fecha']:
                    areas_info[area_id]['primera_fecha'] = fecha_crimen
                if fecha_crimen > areas_info[area_id]['ultima_fecha']:
                    areas_info[area_id]['ultima_fecha'] = fecha_crimen
            else:
                areas_info[area_id] = {
                    'area': area_id,
                    'nombre': area_nombre,
                    'cantidad': 1,
                    'primera_fecha': fecha_crimen,
                    'ultima_fecha': fecha_crimen
                }
    return sorted(areas_info.values(),key=lambda x: (-x['cantidad'],x['nombre']))[:N]

def req_6(catalog, numero_areas, sexo, mes):
    """Retorna el resultado del requerimiento 6
    """
    datos = {}
    for crimen in catalog["crimes_by_id"].values():
        if crimen['Vict Sex'] == sexo:
            fecha = crimen['DATE OCC'].split('-')
            if len(fecha) >= 2 and int(fecha[1]) == mes:
                area = crimen['AREA']
                año = int(fecha[0])
                if area not in datos:
                    datos[area] = {'nombre': crimen['AREA NAME'], 'años': {}, 'total': 0}
                if año not in datos[area]['años']:
                    datos[area]['años'][año] = 0
                datos[area]['años'][año] += 1
                datos[area]['total'] += 1
    arbol = rbt.red_black_tree()
    for area, info in datos.items():
        key = (info['total'], -len(info['años']), info['nombre'])
        value = {
            'Área': area,
            'Nombre del área': info['nombre'],
            'Cantidad de crímenes': info['total'],
            'Crímenes por año': sorted([(cnt, año) for año, cnt in info['años'].items()], key=lambda x: x[1])}
        arbol.insert(key, value)
    return [nodo.value for nodo in arbol.get_sorted()[:numero_areas]]


def req_7(catalog, numero, sexo, edad_min, edad_max):
    """Retorna el resultado del requerimiento 7
    """
    crimenes_diccionario = {}
    for i in range(1, lt.size(catalog) + 1):
        crimen = lt.get_element(catalog, i)
        if all(key in crimen for key in ["sex", "age", "code", "date"]):
            if (crimen["sex"].upper() == sexo.upper() and 
                crimen["age"].isdigit() and 
                int(edad_min) <= int(crimen["age"]) <= int(edad_max)):
                codigo = crimen["code"]
                anio = datetime.strptime(crimen["date"], "%Y-%m-%d").year
                edad = int(crimen["age"])
                if codigo not in crimenes_diccionario:
                    crimenes_diccionario[codigo] = {
                        "total": 0,
                        "por_edad": {},
                        "por_anio": {}}
                crimenes_diccionario[codigo]["total"] += 1
                crimenes_diccionario[codigo]["por_edad"][edad] = crimenes_diccionario[codigo]["por_edad"].get(edad, 0) + 1
                crimenes_diccionario[codigo]["por_anio"][anio] = crimenes_diccionario[codigo]["por_anio"].get(anio, 0) + 1
    lista_ordenada = sorted(
        [{"codigo": k, **v} for k, v in crimenes_diccionario.items()],
        key=lambda x: x["total"],
        reverse=True)
    return lista_ordenada[:int(numero)]

import math
from datetime import datetime

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine"""
    r = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

def req_8(catalog, num, area_name, codigo_crime):
    """
    Retorna el resultado del requerimiento 8
    """
    # estuvo muy horrible, tuve que organizarlo demasiado para que funcione
    start_time = get_time()
    
    # Identificar el área de interés
    area_int = None
    area_enc = False 
    
    areas = catalog["crimes_by_area"].items()
    for area, crimes in areas:
        if not area_enc and crimes and crimes[0]["AREA NAME"].strip().lower() == area_name.strip().lower():
            area_int = area
            area_enc = True  
    
    if not area_int:
        return None
    
    # Filtrar crímenes del área de interés
    crimes_int = []
    for crime in catalog["crimes_by_area"][area_int]:
        try:
            if int(crime["Crm Cd"]) == int(codigo_crime):
                crimes_int.append(crime)
        except (ValueError, KeyError):
            continue
    
    if not crimes_int:
        return None
    
    # Filtrar crímenes de otras áreas
    otros_crimes = []
    for area_num, crimes in catalog["crimes_by_area"].items():
        if area_num != area_int:
            for crime in crimes:
                try:
                    if int(crime["Crm Cd"]) == int(codigo_crime):
                        otros_crimes.append(crime)
                except (ValueError, KeyError):
                    continue
    
    if not otros_crimes:
        return None
    
    # Comparación todos contra todos
    resultados = []
    for target_crime in crimes_int:
        try:
            lat1 = float(target_crime["LAT"])
            lon1 = float(target_crime["LON"])
            date1 = datetime.strptime(target_crime["DATE OCC"].strip(), "%m/%d/%Y %I:%M:%S %p")
            
            for other_crime in otros_crimes:
                try:
                    lat2 = float(other_crime["LAT"])
                    lon2 = float(other_crime["LON"])
                    date2 = datetime.strptime(other_crime["DATE OCC"].strip(), "%m/%d/%Y %I:%M:%S %p")
                    
                    distance = haversine(lat1, lon1, lat2, lon2)
                    
                    # Ordenar por fecha (más antiguo primero)
                    if date1 <= date2:
                        resultado = {
                            "crime1": target_crime,
                            "crime2": other_crime,
                            "distance": distance,
                            "older_date": date1,
                            "newer_date": date2
                        }
                    else:
                        resultado = {
                            "crime1": other_crime,
                            "crime2": target_crime,
                            "distance": distance,
                            "older_date": date2,
                            "newer_date": date1
                        }
                    
                    resultados.append(resultado)
                except (ValueError, KeyError):
                    continue
        except (ValueError, KeyError):
            continue
    
    # Ordenar por distancia
    resultados.sort(key=lambda x: x["distance"])
    
    # Preparar resultados
    closest_resultados = resultados[:num] if len(resultados) >= num else resultados
    farthest_resultados = resultados[-num:] if len(resultados) >= num else []
    
    # Formatear resultados para 
    def format_resultado(resultado):
        return {
            "tipo_crimen": resultado["crime1"]["Crm Cd Desc"],
            "area_otra": resultado["crime2"]["AREA NAME"],
            "fecha_1": resultado["older_date"].strftime("%m/%d/%Y"),
            "fecha_2": resultado["newer_date"].strftime("%m/%d/%Y"),
            "distancia_km": resultado["distance"]
        }
    
    closest_results = [format_resultado(p) for p in closest_resultados]
    farthest_results = [format_resultado(p) for p in farthest_resultados]
    
    end_time = get_time()
    elapsed_time = delta_time(start_time, end_time)
    
    return closest_results, farthest_results, elapsed_time
            
    
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
