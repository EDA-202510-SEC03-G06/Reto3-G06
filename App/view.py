import sys
from App import logic 
import os

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    """Interfaz para carga de datos"""
    print("\n=== CARGA DE DATOS ===")
    filename = input("Ingrese el nombre del archivo CSV: ").strip()

    #agrego extensión si no está presente
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    filename_s = [filename,os.path.join('Data', filename)]
    
    for path in filename_s:
        if os.path.exists(path):
            filename = path
            print(f"\nCargando {filename}...")
            return logic.load_data(control, filename)
    else: #caso en el que no se encuentre el archivo
        print("\nError: Archivo no encontrado")
        print("=================================")
        return print_menu()


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    crime = logic.get_data(control, id)
    if crime:
        print("\n=== DETALLE ===")
        print(f"ID: {crime['DR_NO']}")
        print(f"Fecha: {crime['DATE OCC']}")
        print(f"Área: {crime.get('AREA NAME', 'Desconocida')}")
        print(f"Ubicación: {crime.get('LOCATION', 'Sin dirección')}")
    else:
        print(f"\nCrimen con ID {id} no encontrado")
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    print("\n=== Requerimiento 1 ===")
    print("Listado de crimenes por rango de fechas")
    print("formato de fecha: MM/DD/YYYY")
    
    dato_inicial = input("Ingrese la fecha inicial: ").strip()
    dato_final = input("Ingrese la fecha final: ").strip()
    
    funcion = logic.req_1(control, dato_inicial, dato_final)
    result = funcion["result"]
    elapsed_time = funcion["time"]
    
    if not result:
        print("No se encontraron crimenes")
        return print_menu()
    
    print(f"\nTiempo de ejecución: {elapsed_time:.2f} ms")
    print(f"\nTotal de crimenes: {len(result)}")
    
    print(f"\nTotal de crímenes encontrados: {len(result)}")
    print("\nPrimeros 5 crímenes ordenados (más recientes primero):")
    print("-" * 80)
    
    for numero, crimen in enumerate(result[:5], 1):
        print(f"Crimen #{numero}:")
        print(f"  ID: {crimen['id']}")
        print(f"  Fecha: {crimen['date']}")
        print(f"  Hora: {crimen['time']}")
        print(f"  Área: {crimen['area']}")
        print(f"  Código: {crimen['codigo']}")
        print(f"  Dirección: {crimen['direccion']}")
        print("-" * 80)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("\n=== Requerimiento 2 ===")
    print("Listado de crimenes por rango de fechas")
    print("formato de fecha: MM/DD/YYYY")
    
    dato_inicial = input("Ingrese la fecha inicial: ").strip()
    dato_final = input("Ingrese la fecha final: ").strip()
    
    total_c, results, elapsed = logic.req_2(control, dato_inicial, dato_final)
    if total_c == 0:
        print("No se encontraron crimenes graves resueltos en el rango solicitado")
        return print_menu()
    
    print(f"\nTotal de crímenes graves resueltos encontrados: {total_c}")
    print(f"Tiempo de ejecución: {elapsed:.3f} ms")
    
    if total_c <= 10:
        print("\nPrimeros 10 crímenes ordenados (más recientes primero):")
        print("-" * 80)
        for num, result in enumerate(results, 1):
            print(f"Crimen #{num}:")
            print(f"  ID: {result["id"]}")
            print(f"  Fecha: {result["date"]}")
            print(f"  Hora: {result["time"]}")
            print(f"  Área: {result["area"]}")
            print(f"  Subárea: {result["subarea"]}")
            print(f"  Gravedad: {result["gravedad"]}")
            print(f"  Código: {result["codigo"]}")
            print(f"  Estado: {result["estado"]}")
            print("-" * 80)
    else:    
        print("\nPrimeros 5 crímenes ordenados (más recientes primero):")
        print("-" * 80)
        for num, result in enumerate(results[:5], 1):
            print(f"Crimen #{num}:")
            print(f"  ID: {result["id"]}")
            print(f"  Fecha: {result["date"]}")
            print(f"  Hora: {result["time"]}")
            print(f"  Área: {result["area"]}")
            print(f"  Subárea: {result["subarea"]}")
            print(f"  Gravedad: {result["gravedad"]}")
            print(f"  Código: {result["codigo"]}")
            print(f"  Estado: {result["estado"]}")
            print("-" * 80)
        
        print("\n...\n")
        print("\nUltimos 5 crímenes ordenados (más Antiguos):")
        print("-" * 80)
        for num, result in enumerate(results[-5:], total_c-5):
            print(f"Crimen #{num}:")
            print(f"  ID: {result["id"]}")
            print(f"  Fecha: {result["date"]}")
            print(f"  Hora: {result["time"]}")
            print(f"  Área: {result["area"]}")
            print(f"  Subárea: {result["subarea"]}")
            print(f"  Gravedad: {result["gravedad"]}")
            print(f"  Código: {result["codigo"]}")
            print(f"  Estado: {result["estado"]}")
            print("-" * 80)
    
def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n=== Requerimiento 3 ===")
    print("Listado de crimenes mas recientes por area")
    
    # Obtener y validar entrada
    nomb_area = input("Ingrese la área: ")
    if not nomb_area or not isinstance(nomb_area, str):
        print("Error: Área no válida")
        return
    
    try:
        num = int(input("Ingrese el número de crimenes: "))
        if num <= 0:
            print("Error: El número debe ser positivo")
            return
    except ValueError:
        print("Error: Debe ingresar un número válido")
        return
    
    # Obtener resultados
    total_c, results, elapsed = logic.req_3(control, num, nomb_area)
    
    # Mostrar resultados
    print("\n" + "="*80)
    print(f"RESULTADOS PARA EL ÁREA: {nomb_area.upper()}")
    print(f"Total de crímenes en el área: {total_c}")
    print(f"Mostrando los {min(num, total_c)} más recientes:")
    print("="*80 + "\n")
    
    if total_c == 0:
        print("No se encontraron crímenes para el área especificada")
        return
    
    
    
    # Mostrar cada crimen
    for numero, result in enumerate(results, 1):
        print(f"Crimen #{numero}:")
        print(f"  ID: {result["id"]}")
        print(f"  Fecha: {result["dato"]}")
        print(f"  Hora: {result["tiempo"]}")
        print(f"  Área: {result["area"]}")
        print(f"  Subárea: {result["subarea"]}")
        print(f"  Gravedad: {result["gravedad"]}")
        print(f"  Código: {result["codigo"]}")
        print(f"  Estado: {result["estado"]}")
        print(f"  • Dirección: {result["direccion"]}")
        print("-" * 80)
        
    print(f"\nTiempo de ejecución: {elapsed:.2f} ms")

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("=== Requerimiento 4 ===")
    print("Listado de crímenes más antiguos por un tipo de crimen específico")
    tipo_crimen = input("Ingrese el tipo de crimen: ")
    edad_final = int(input("Ingrese la edad máxima: "))
    num = int(input("Ingrese el número de crímenes a listar: "))
    total_c, resultados = logic.req_4(control, tipo_crimen, num, edad_final)
    print(f"RESULTADOS PARA EL TIPO DE CRIMEN: {tipo_crimen}")
    print(f"Total de crímenes encontrados: {total_c}")
    print(f"Mostrando los {min(total_c, num)} más antiguos:")
    print("="*80)
    
    if total_c == 0:
        print("No se encontraron crímenes para el tipo especificado")
    else:
        for i, crimen in enumerate(resultados["elements"], start=1):
            print(f"Crimen #{i}:")
            print(f"  ID: {crimen['report_id']}")
            print(f"  Fecha: {crimen['date']}")
            print(f"  Hora: {crimen['time']}")
            print(f"  Área: {crimen['area']}")
            print(f"  Subárea: {crimen['subarea']}")
            print(f"  Gravedad: {crimen['severity']}")
            print(f"  Código de crimen: {crimen['crime_code']}")
            print(f"  Edad de la víctima: {crimen['victim_age']}")
            print(f"  Estado del caso: {crimen['case_status']}")
            print(f"  Dirección: {crimen['address']}")
            print("-" * 80)
def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print("\n=== Requerimiento 5 ===")
    N = input("Ingrese cantidad de áreas: ")
    if not N.isdigit() or int(N) <= 0:
        print("Error: N debe ser positivo")
        return
    fecha_inicial = input("Fecha inicial (YYYY-MM-DD): ")
    fecha_final = input("Fecha final (YYYY-MM-DD): ")
    if len(fecha_inicial)!=10 or len(fecha_final)!=10 or fecha_inicial[4]!='-' or fecha_final[4]!='-':
        print("Error: Formato YYYY-MM-DD")
        return
    resultados = logic.req_5(control,int(N),fecha_inicial,fecha_final)
    if not resultados:
        print("\nNo se encontraron resultados")
        return
    print(f"\nTop {N} áreas ({fecha_inicial} a {fecha_final})")
    print("="*80)
    print(f"{'ID':<8}{'Nombre':<30}{'Total':<8}{'Primer':<12}{'Último':<12}")
    print("="*80)
    for area in resultados:
        print(f"{area['area']:<8}{area['nombre']:<30}{area['cantidad']:<8}{area['primera_fecha']:<12}{area['ultima_fecha']:<12}")
        
def print_req_6(control):
    sexo = input("Ingrese el sexo (M/F): ").strip().upper()
    mes = int(input("Ingrese el mes (1-12): ").strip())
    numero_areas = int(input("Ingrese la cantidad de áreas a listar: ").strip())
    if sexo not in ['M', 'F']:
        print("Sexo inválido. Debe ser M o F.")
        return
    if mes < 1 or mes > 12:
        print("Mes inválido. Debe estar entre 1 y 12.")
        return
    resultados = logic.req_6(control, numero_areas, sexo, mes)
    if resultados:
        for idx, resultado in enumerate(resultados, 1):
            print(f"\nResultado {idx}:")
            print(f"Área: {resultado['Área']}")
            print(f"Nombre del área: {resultado['Nombre del área']}")
            print(f"Cantidad de crímenes: {resultado['Cantidad de crímenes']}")
            print("Crímenes por año:")
            for cnt, año in resultado['Crímenes por año']:
                print(f"  Año {año}: {cnt} crímenes")
    else:
        print("No se encontraron resultados.")

def print_req_7(control):
    """ Funcion que imprime la solución del Requerimiento 7"""
    numero = input("Ingrese el número de crímenes más comunes: ")
    sexo = input("Ingrese el sexo de la víctima (M/F): ").upper()
    edad_min = input("Edad mínima: ")
    edad_max = input("Edad máxima: ")
    resultado = logic.req_7(control, numero, sexo, edad_min, edad_max)  # Cambio clave aquí
    print(f"\nCrímenes más comunes para víctimas de sexo {sexo} y edad {edad_min}-{edad_max}")
    print("-"*80)
    if not resultado:
        print("No se encontraron crímenes que cumplan los criterios")
        return
    max_edades = max(len(c["por_edad"]) for c in resultado)
    max_anios = max(len(c["por_anio"]) for c in resultado)
    headers = ["Código", "Total"] + [f"Edad {i+1}" for i in range(max_edades)] + [f"Año {i+1}" for i in range(max_anios)]
    print(" | ".join(headers))
    print("-" * len(" | ".join(headers)))
    for crimen in resultado:
        edades = [f"{v}({k})" for k, v in sorted(crimen["por_edad"].items())]
        años = [f"{v}({k})" for k, v in sorted(crimen["por_anio"].items())]
        fila = [
            crimen["codigo"],
            str(crimen["total"]),
            *edades,
            *[""] * (max_edades - len(edades)),
            *años,
            *[""] * (max_anios - len(años))]
        print(" | ".join(fila))

def print_req_8(control):
    print("\n=== Requerimiento 8 (BONO) ===")
    try:
        num = int(input("Número de parejas a retornar (N): ").strip())
        area_name = input("Nombre del área de interés: ").strip()
        codigo_crime = input("Código del tipo de crimen (crm_cd): ").strip()
        
        resultados = logic.req_8(control, num, area_name, codigo_crime)
        
        if not resultados or (not resultados[0] and not resultados[1]):
            print("\nNo se encontraron resultados con los criterios especificados")
            return
        
        cercanos, lejanos, tiempo = resultados
        
        print("\n=== PAREJAS MÁS CERCANAS ===")
        for i, pareja in enumerate(cercanos, 1):
            print(f"\nPareja #{i}:")
            print(f"Tipo de crimen: {pareja['tipo_crimen']}")
            print(f"Área externa: {pareja['area_otra']}")
            print(f"Fecha más antigua: {pareja['fecha_1']}")
            print(f"Fecha más reciente: {pareja['fecha_2']}")
            print(f"Distancia: {pareja['distancia_km']:.2f} km")
        
        print("\n=== PAREJAS MÁS LEJANAS ===")
        for i, pareja in enumerate(lejanos, 1):
            print(f"\nPareja #{i}:")
            print(f"Tipo de crimen: {pareja['tipo_crimen']}")
            print(f"Área externa: {pareja['area_otra']}")
            print(f"Fecha más antigua: {pareja['fecha_1']}")
            print(f"Fecha más reciente: {pareja['fecha_2']}")
            print(f"Distancia: {pareja['distancia_km']:.2f} km")
        
        print(f"\nTiempo de ejecución: {tiempo} ms")
        print("\n" + "="*80)
    
    except ValueError:
        print("Error: Entrada inválida")

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
