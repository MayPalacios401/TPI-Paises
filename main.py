# Trabajo Práctico Integrador - Programación I
# Sistema de Gestión de Países
#
# Estructura principal:
# - Lista de diccionarios
# - Archivo CSV como origen de datos
# - Funciones modulares
# - Búsquedas, filtros, ordenamientos y estadísticas
#
# Integrantes:
# Mayra Palacios
# Ammiel Vainstein


import csv

# Funciones auxiliares para obtener información de los países
def obtener_nombre(pais):
    return pais["nombre"]

def obtener_poblacion(pais):
    return pais["poblacion"]

def obtener_superficie(pais):
    return pais["superficie"]

def mostrar_pais(pais):
    print(f"Nombre: {pais['nombre']}")
    print(f"Población: {pais['poblacion']}")
    print(f"Superficie: {pais['superficie']} km²")
    print(f"Continente: {pais['continente']}")
    print("-" * 40)

# Función auxiliar para mostrar resultados de forma uniforme.
# Se reutiliza en búsquedas, filtros y ordenamientos.
def mostrar_lista_paises(lista):
    if len(lista) == 0:
        print("\nNo se encontraron resultados.")
    else:
        print(f"\nSe encontraron {len(lista)} resultado/s:\n")
        for pais in lista:
            mostrar_pais(pais)

# Función reutilizable para validar entradas numéricas.
# Centraliza la validación y evita repetir código
# en distintas partes del sistema.
def pedir_entero_positivo(mensaje):
    while True:
        try:
            numero = int(input(mensaje).strip())
            if numero <= 0:
                print("El número debe ser mayor que cero.")
            else:
                return numero
        except ValueError:
            print("Debe ingresar un número entero válido.")

#--MÓDULO DE DATOS--#

# Punto de entrada de los datos del sistema.
# Se lee el archivo CSV y se transforma cada registro
# en un diccionario que luego será almacenado dentro
# de una lista de países.

def leer_csv():
    paises = []
    try:
        with open('paises.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for numero_linea, linea in enumerate(lector, start=1):
                if len(linea) == 0:
                    continue

                if linea[0].lower() == 'nombre':
                    continue  # Saltar la fila de encabezado

                if len(linea) != 4:
                    print(f"Error de formato en la línea {numero_linea}. Se omite ese registro.")
                    continue

                try:
                    # Cada país se representa mediante un diccionario.
                    # Esta estructura nos permite acceder fácilmente a los
                    # atributos utilizando claves descriptivas.
                    pais = {
                        'nombre': linea[0].strip(),
                        'poblacion': int(linea[1]),
                        'superficie': int(linea[2]),
                        'continente': linea[3].strip()
                    }

                    if pais['nombre'] == "" or pais['continente'] == "":
                        print(f"Campos vacíos en la línea {numero_linea}. Se omite ese registro.")
                        continue

                    if pais['poblacion'] <= 0 or pais['superficie'] <= 0:
                        print(f"Valores numéricos inválidos en la línea {numero_linea}. Se omite ese registro.")
                        continue

                    paises.append(pais)

                except ValueError:
                    print(f"Error de tipo de dato en la línea {numero_linea}. Se omite ese registro.")

    except FileNotFoundError:
        print("\nNo se encontró el archivo paises.csv. Se iniciará con una lista vacía.")

    return paises

# Función encargada del alta de nuevos registros.
# Se validan los datos ingresados para evitar
# información incompleta o duplicada.
def agregar_pais(paises):
    while True:
        nombre = input("\nIngrese el nombre del país a agregar: ").strip().lower()
        if nombre == "":
            print("El nombre no puede estar vacío.")
        else:
            break

    # Recorremos toda la lista para verificar
    # que el país no exista previamente.        
    for pais in paises: 
        if pais['nombre'].lower() == nombre.lower():
            print("\nEl país ya existe en la lista.")
            return
        
    poblacion = pedir_entero_positivo("\nIngrese la población del país: ")
    superficie = pedir_entero_positivo("\nIngrese la superficie del país (en km²): ")

    while True:
        continente = input("\nIngrese el continente del país: ").strip()
        if continente == "":
            print("El continente no puede estar vacío.")
        else:
            break

    nuevo_pais = {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    }

    paises.append(nuevo_pais)
    print(f"\nPaís {nombre.title()} agregado exitosamente.")

# Permite modificar información existente.
# Se busca el país por nombre y se actualizan
# únicamente los campos solicitados.
def actualizar_pais(paises):
    nombre = input("\nIngrese el nombre del país a actualizar: ").strip()

    for pais in paises:
        if pais['nombre'].lower() == nombre.lower():
            print(f"\nActualizando información de {pais['nombre']}...")

            poblacion = pedir_entero_positivo("\nIngrese la nueva población del país: ")
            superficie = pedir_entero_positivo("\nIngrese la nueva superficie del país (en km² sin puntos): ")

            pais['poblacion'] = poblacion
            pais['superficie'] = superficie

            print(f"\nPaís {pais['nombre']} actualizado exitosamente.")
            return

    print("\nEl país no se encontró en la lista.")

#--MÓDULO DE ORDENAMIENTO--#

# Se permite ordenar la información según distintos
# criterios elegidos por el usuario.
# Utilizamos sorted() para evitar modificar la lista original.
def ordenar_paises(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para ordenar.")
        return

    print("\n¿Por qué criterio desea ordenar los países?")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    criterio = input("\nIngrese el número correspondiente al criterio de ordenamiento: ").strip()

    print("\n¿Desea ordenar de manera ascendente o descendente?")
    print("1. Ascendente")
    print("2. Descendente")
    orden = input("\nIngrese el número correspondiente al ordenamiento: ").strip()

    if criterio == "1":
        clave = obtener_nombre
    elif criterio == "2":
        clave = obtener_poblacion
    elif criterio == "3":
        clave = obtener_superficie
    else:
        print("\nOpción inválida.")
        return

    if orden == "1":
        invertir = False
    elif orden == "2":
        invertir = True
    else:
        print("\nOpción inválida.")
        return
    
    # sorted() genera una nueva lista ordenada.
    # key define el criterio de comparación y
    # reverse determina si el orden es ascendente o descendente.
    resultado = sorted(paises, key=clave, reverse=invertir)
    mostrar_lista_paises(resultado)

#--MÓDULO DE BÚSQUEDA Y FILTRO--#

# Implementa una búsqueda parcial.
# Permite encontrar coincidencias aunque el usuario
# ingrese solo una parte del nombre.
def buscar_pais(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para buscar.")
        return

    busqueda = input("\nIngrese el nombre o parte del nombre del país: ").strip().lower() #eliminamos espacios y convertimos todo a minúsculas

    if busqueda == "":
        print("\nLa búsqueda no puede estar vacía.")
        return

    resultados = []

    for pais in paises:
        if busqueda in pais["nombre"].lower():
            resultados.append(pais)

    mostrar_lista_paises(resultados)

# Filtra los registros que pertenecen al continente indicado.
def filtrar_por_continente(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para filtrar.")
        return

    continente = input("\nIngrese el continente a filtrar: ").strip().lower()#quitamos espacios y pasamos todo a minúsculas

    if continente == "":
        print("\nEl continente no puede estar vacío.")
        return

    resultados = []

    for pais in paises:
        if pais["continente"].lower() == continente:
            resultados.append(pais)

    mostrar_lista_paises(resultados)


def filtrar_por_poblacion(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para filtrar.")
        return

    minimo = pedir_entero_positivo("\nIngrese la población mínima: ")# Se utiliza un rango mínimo y máximo para obtener
    maximo = pedir_entero_positivo("Ingrese la población máxima: ")# únicamente los países que cumplen la condición solicitada.

    if minimo > maximo:
        print("\nEl valor mínimo no puede ser mayor que el máximo.")
        return

    resultados = []

    for pais in paises:
        if minimo <= pais["poblacion"] <= maximo:
            resultados.append(pais)

    mostrar_lista_paises(resultados)

def filtrar_por_superficie(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para filtrar.")
        return

    minimo = pedir_entero_positivo("\nIngrese la superficie mínima: ")
    maximo = pedir_entero_positivo("Ingrese la superficie máxima: ")

    if minimo > maximo:
        print("\nEl valor mínimo no puede ser mayor que el máximo.")
        return

    resultados = []

    for pais in paises:
        if minimo <= pais["superficie"] <= maximo:
            resultados.append(pais)

    mostrar_lista_paises(resultados)

#--MÓDULO DE ESTADÍSTICAS--#

# Calcula indicadores generales sobre la colección de países.
# Se utilizan recorridos completos de la lista para obtener
# máximos, mínimos, promedios y agrupaciones por continente.
def mostrar_estadisticas(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para calcular estadísticas.")
        return

    # Obtención del país con mayor y menor población.
    # Las funciones auxiliares indican qué atributo comparar.
    pais_mayor_poblacion = max(paises, key=obtener_poblacion)
    pais_menor_poblacion = min(paises, key=obtener_poblacion)

    suma_poblacion = 0
    suma_superficie = 0
    # Diccionario utilizado como contador.
    # La clave es el continente y el valor representa
    # la cantidad de países pertenecientes a él.
    cantidad_por_continente = {}

    for pais in paises:
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        continente = pais["continente"]
        if continente in cantidad_por_continente:
            cantidad_por_continente[continente] += 1
        else:
            cantidad_por_continente[continente] = 1

    promedio_poblacion = suma_poblacion / len(paises)
    promedio_superficie = suma_superficie / len(paises)

    print("\nESTADÍSTICAS GENERALES")
    print("-" * 40)
    print(f"País con mayor población: {pais_mayor_poblacion['nombre']} ({pais_mayor_poblacion['poblacion']})")
    print(f"País con menor población: {pais_menor_poblacion['nombre']} ({pais_menor_poblacion['poblacion']})")
    print(f"Promedio de población: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km²")

    print("\nCantidad de países por continente:")
    for continente, cantidad in cantidad_por_continente.items():
        print(f"{continente}: {cantidad}")

#--MENÚ PRINCIPAL--#

# Punto principal de interacción con el usuario.
# Mantiene la ejecución activa hasta que se seleccione la opción Salir.
def menu():
    paises = leer_csv()

    while True:
        print("\nMenú de opciones:")
        print("1. Agregar país")
        print("2. Actualizar país")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Mostrar estadísticas")
        print("7. Salir")

        opcion = input("\nIngrese el número correspondiente a la opción deseada: ").strip()

        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            print("\nOpciones de filtrado:")
            print("1. Filtrar por continente")
            print("2. Filtrar por población")
            print("3. Filtrar por superficie")
            filtro = input("\nIngrese el número correspondiente al filtro deseado: ").strip()

            if filtro == "1":
                filtrar_por_continente(paises)
            elif filtro == "2":
                filtrar_por_poblacion(paises)
            elif filtro == "3":
                filtrar_por_superficie(paises)
            else:
                print("\nOpción inválida.")

        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            print("\nSaliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Por favor, intente nuevamente.")

menu()


