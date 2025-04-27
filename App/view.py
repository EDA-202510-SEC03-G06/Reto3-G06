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
        return None


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
    
    result = logic.req_1(control, dato_inicial, dato_final)
    if not result:
        print("No se encontraron crimenes")
        return
    
    print(f"\nTotal de crimenes: {len(result)}")
    
    print(f"\nTotal de crímenes encontrados: {len(result)}")
    print("\nPrimeros 5 crímenes ordenados (más recientes primero):")
    print("-" * 80)
    
    for numero, crimen in enumerate(result[:5], 1):
        print(f"Crimen #{numero}:")
        print(f"ID: {crimen['id']}")
        print(f"Fecha: {crimen['date']}")
        print(f"Hora: {crimen['time']}")
        print(f"Área: {crimen['area']}")
        print(f"Código: {crimen['codigo']}")
        print(f"Dirección: {crimen['direccion']}")
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
    
    total_c, results = logic.req_2(control, dato_inicial, dato_final)
    if total_c == 0:
        print("No se encontraron crimenes graves resueltos en el rango solicitado")
        return
    
    print(f"\nTotal de crímenes graves resueltos encontrados: {total_c}")
    
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
    # TODO: Imprimir el resultado del requerimiento 3
    pass


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
    pass


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
