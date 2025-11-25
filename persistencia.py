import json
def guardar_clientes(lista_clientes, archivo = "clientes.json"):
    """
    Guarda la lista de clientes en un archivo JSON para mantener persistencia de datos.
    Dato: el "ensure_ascii = False" nos va solucionar por si existen nombres con ñ.

    Parámetros:
        lista_clientes (list): lista de diccionarios con la información de los clientes.
        archivo (str): nombre del archivo donde se guardarán los datos.
    """
    try:
        with open(archivo, "w", encoding = "utf-8") as file:
             json.dump(lista_clientes, file, indent = 4, ensure_ascii= False)
        print("Datos guardados correctamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")


def cargar_clientes(archivo = "clientes.json"):
    """
    Carga la lista de clientes desde un archivo JSON.
    Si no existe el archivo, devuelve una lista vacía.

    Retorna:
        list: lista de clientes cargada desde el archivo.
    """
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            listaInterna = json.load(file)
        print("Datos cargados correctamente.")
        return listaInterna
    except FileNotFoundError:
        print("No se encontro el archivo. Se creara una nuevo al guardar")
        return []
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Se reiniciara la lista.")
        return []
