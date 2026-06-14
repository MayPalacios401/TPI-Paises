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

def mostrar_lista_paises(lista):
    if len(lista) == 0:
        print("\nNo se encontraron resultados.")
    else:
        print(f"\nSe encontraron {len(lista)} resultado/s:\n")
        for pais in lista:
            mostrar_pais(pais)

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

def agregar_pais(paises):
    while True:
        nombre = input("\nIngrese el nombre del país a agregar: ").strip()
        if nombre == "":
            print("El nombre no puede estar vacío.")
        else:
            break

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

    resultado = sorted(paises, key=clave, reverse=invertir)
    mostrar_lista_paises(resultado)

#--MÓDULO DE BÚSQUEDA Y FILTRO--#
def buscar_pais(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para buscar.")
        return

    busqueda = input("\nIngrese el nombre o parte del nombre del país: ").strip().lower()

    if busqueda == "":
        print("\nLa búsqueda no puede estar vacía.")
        return

    resultados = []

    for pais in paises:
        if busqueda in pais["nombre"].lower():
            resultados.append(pais)

    mostrar_lista_paises(resultados)

def filtrar_por_continente(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para filtrar.")
        return

    continente = input("\nIngrese el continente a filtrar: ").strip().lower()

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

    minimo = pedir_entero_positivo("\nIngrese la población mínima: ")
    maximo = pedir_entero_positivo("Ingrese la población máxima: ")

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
def mostrar_estadisticas(paises):
    if len(paises) == 0:
        print("\nNo hay países cargados para calcular estadísticas.")
        return

    pais_mayor_poblacion = max(paises, key=obtener_poblacion)
    pais_menor_poblacion = min(paises, key=obtener_poblacion)

    suma_poblacion = 0
    suma_superficie = 0
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
