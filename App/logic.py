
import csv
import sys
import time
import os
from datetime import datetime
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

def haversine(lat1, lon1, lat2, lon2):
    r = 6371 # Radio de la tierra en km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c
def req_8(catalog, num, area_name, crime_type):
    
    #la verdad este si estubo dificil, tuve que organizarlo bastante con comentarios
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    start_time = get_time()
    num_area = None
    
    #numero de area
    crimenes_inte = []
    for area, crimes in catalog["crimes_by_area"].items():
        if crimes and crimes[0]["AREA NAME"].strip().lower() == area_name.strip().lower():
            num_area = area
            continue
            
    if not num_area:
        return None
    #crimenes de interes
    for crime in catalog["crimes_by_area"][num_area]:
        if int(crime["Crm Cd"]) == crime_type:
            crimenes_inte.append(crime)
            
    if not crimenes_inte:
        return None
    #crimenes del mismo tipo en otras areas
    otros_crimenes = []
    for area, crimes in catalog["crimes_by_area"].items():
        if area != num_area:
            for crime in crimes:
                if crime["Crm Cd"] == crime_type:
                    otros_crimenes.append(crime)
                
    if not otros_crimenes:
        return None
    
    #distancia
    resultados = []
    for crimen in crimenes_inte:
        lat1 = float(crimen["LAT"])
        long1 = float(crimen["LON"])
        fecha_ref = datetime.strptime(crimen["DATE OCC"].strip(), "%m/%d/%Y %I:%M:%S %p").date()
        for otro in otros_crimenes:
            lat2 = float(otro["LAT"])
            long2 = float(otro["LON"])
            fecha_otro = datetime.strptime(otro["DATE OCC"].strip(), "%m/%d/%Y %I:%M:%S %p").date()
            distancia = haversine(lat1, long1, lat2, long2)
            
            #miro cual es el primer y segundo crimen
            if fecha_ref <= fecha_otro:
                fecha_primero, fecha_segundo = fecha_ref, fecha_otro
            else:
                fecha_primero, fecha_segundo = fecha_otro, fecha_ref
            
            resultados.append({
                "tipo": crimen["Crm Cd Desc"],
                "area otra": otro["AREA NAME"],
                "fecha 1": fecha_primero,
                "fecha 2": fecha_segundo,
                "distancia (km)": distancia
            })
            
    #ordeno
    resultados.sort(key=lambda x: x["distancia (km)"])
    
    #respuesta
    cercanos = resultados[:num]
    lejanos = resultados[-num:] if len(resultados) > num else resultados
    
    end_time = get_time()
    elapsed = delta_time(start_time, end_time)
    
    return cercanos, lejanos, elapsed
            
    
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
