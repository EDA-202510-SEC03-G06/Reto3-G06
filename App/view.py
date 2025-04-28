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
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    print("\n=== Requerimiento 8 ===")
    num = int(input("Ingrese el número N de crímenes a consultar: ").strip())
    area_name = input("Ingrese el nombre del área de interés: ").strip()
    crime_type = input("Ingrese el tipo de crimen a consultar: ").strip()

    resultados = logic.req_8(control, num, area_name, crime_type)
    
    if resultados is None:
        print("No se encontraron crímenes")
        return print_menu()
    
    cercanos, lejanos, tiempo = resultados
    
    if not cercanos and not lejanos:
        print("No se encontraron crímenes")
        return print_menu()
    
    print("\n== Crimenes cercanos ==")
    for crimes in cercanos:
        print(f"Tipo: {crimes['tipo']}")
        print(f"Área: {crimes['area otra']}")
        print(f"Fecha: {crimes['fecha 1']}")
        print(f"Fecha: {crimes['fecha 2']}")
        print(f"Distancia (km): {crimes['distancia (km)']:.2f} km")
        print("-" * 80)
        
    print("\n== Crimenes lejanos ==")
    for crimes in lejanos:
        print(f"Tipo: {crimes['tipo']}")
        print(f"Área: {crimes['area otra']}")
        print(f"Fecha: {crimes['fecha 1']}")
        print(f"Fecha: {crimes['fecha 2']}")
        print(f"Distancia (km): {crimes['distancia (km)']:.2f} km")
        print("-" * 80)
        
    print(f"\nTiempo de ejecución: {tiempo} ms")
    print("\n" + "="*80)

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
