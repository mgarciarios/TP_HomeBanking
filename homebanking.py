import random
import os
import time
import json
import sys
from persistencia import guardar_clientes, cargar_clientes

def pedir_dni():
    while True:
        try:
            dni = int(input("Ingrese su DNI sin puntos (ej: 12345678): "))
        except ValueError:
            print("DNI inválido. Solo números.")
            time.sleep(1.0)
            continue
        
        dni_str = str(dni)

        if dni <= 0:
            print("El DNI debe ser un número positivo.")
            time.sleep(1)
            continue
        
        if len(dni_str) not in (7, 8):
            print("El DNI debe tener 7 u 8 dígitos.")
            time.sleep(1)
            continue

        return dni


def limpiar_pantalla():
    """
    Limpia la consola según el sistema operativo (Windows o Unix-like).

    Args:
        None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pausar_y_volver():
    """
    Pausa hasta que el usuario presione ENTER y luego limpia la pantalla.

    Args:
        None
    """
    """Pausa la ejecución y pide confirmación para volver al menú principal.

    Durante la ejecución de tests (pytest) o si la entrada no es un TTY, no
    bloquea esperando input para evitar fallos en pruebas automatizadas.
    """
    if os.environ.get('PYTEST_CURRENT_TEST') or not sys.stdin.isatty():
        return

    input("\nPresione ENTER para volver al menú de operaciones...")
    limpiar_pantalla()

def registrar_usuario(lista_clientes):
    """
    Registra un cliente nuevo validando que el DNI no exista, que el usuario no se repita
    y que la contraseña cumpla con los requisitos básicos.

    Args:
        lista_clientes (list): Lista de clientes persistidos, cada uno como diccionario.

    Returns:
        dict | None: El cliente creado si todo salió bien; None si el DNI ya estaba registrado.
    """ 

    nuevo_cliente = {}

    limpiar_pantalla()
    dni_actual = pedir_dni()

    for cliente in lista_clientes:
        if cliente["dni_actual"] == dni_actual:
            print("El DNI ya está registrado. Por favor, inicie sesión.")
            return 

    nuevo_cliente["dni_actual"] = dni_actual

    limpiar_pantalla()
    usuario = input("Ingrese su usuario (se recomienda la primer letra del nombre y su apellido): ")    
    
    existe_cliente = True
    while existe_cliente:
        existe_cliente = False
        for cliente in lista_clientes:
            if cliente["Usuario"] == usuario:
                existe_cliente = True
                print("Ese nombre de usuario ya fue registrado")
                usuario = input("Ingrese otro usuario: ")
        
    nuevo_cliente["Usuario"] = usuario

    while True:
        limpiar_pantalla()
        contrasena_1 = input("Ingrese una contraseña (debe tener entre 8 y 12 caracteres, contener una mayúscula y un número): ")

        if not (8 <= len(contrasena_1) <= 12):
            print("Error: La contraseña debe tener entre 8 y 12 caracteres.")
            time.sleep(1.5)
        else:
            tiene_mayuscula = False
            tiene_numero = False

            for caracter in contrasena_1:
                if caracter.isupper():
                    tiene_mayuscula = True
                elif caracter.isdigit():
                    tiene_numero = True

            if not tiene_mayuscula:
                print("Error: La contraseña debe incluir al menos una letra mayúscula.")
                time.sleep(1.5)
            elif not tiene_numero:
                print("Error: La contraseña debe incluir al menos un número.")
                time.sleep(1.5)
                
            else:
                limpiar_pantalla()
                contrasena_2 = input("Repita la contraseña: ")
                if contrasena_1 == contrasena_2:
                    nuevo_cliente["Contraseña"] = contrasena_1
                    print("¡Usuario registrado exitosamente!")
                    return nuevo_cliente
                else:
                    print("Las contraseñas no coinciden. Intente de nuevo.")
                    time.sleep(1.5)

def iniciar_sesion(lista):
    """
    Inicia sesión pidiendo DNI, usuario y contraseña. Permite reintentos.

    Args:
        lista (list): Lista de clientes (diccionarios) con 'dni_actual', 'Usuario' y 'Contraseña'.

    Returns:
        dict | None: El cliente autenticado si los datos son correctos; None si el usuario decide salir.
    """
    while True:
        limpiar_pantalla()
        dni_actual = pedir_dni()

        cliente = next((c for c in lista if c.get("dni_actual") == dni_actual), None)

        if cliente is None:
            print("DNI no encontrado.")
        else:
            usuario = input("Ingrese su usuario: ")
            if usuario == cliente.get("Usuario"):
                contraseña = input("Ingrese su contraseña: ")
                if contraseña == cliente.get("Contraseña"):
                    print("Ingreso exitoso. Bienvenido/a.")
                    return cliente
                else:
                    print("Contraseña incorrecta.")
            else:
                print("Usuario incorrecto.")

        continuar = input("¿Desea intentar ingresar nuevamente? (S/N): ").strip().upper()
        if continuar == 'N':
            print("Ha salido del sistema exitosamente.")
            return None

def crear_cuenta(lista_clientes, dni_actual, tipo_cuenta, moneda):
    """
    Crea una cuenta para el cliente si no la tiene ya, con saldo inicial 0.0.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (int): DNI del titular de la cuenta.
        tipo_cuenta (str): Nombre de la cuenta a crear (ej.: "Cuenta en pesos").
        moneda (str): Código de moneda para mostrar en pantalla (ej.: "ARS", "USD").

    Returns:
        dict | None: El cliente actualizado si se creó; None si no se encontró el cliente.
    """    
    obtener_moneda = lambda tipo_cuenta: tipo_cuenta.split(' ')[2].replace('dólares', 'dolares')

    cliente_encontrado = None

    for cliente in lista_clientes:
        if cliente["dni_actual"] == dni_actual: 
            cliente_encontrado = cliente
    
    if cliente_encontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipo_cuenta in cliente_encontrado:
        print(f"El cliente ya posee una cuenta en {tipo_cuenta}.")

    else:
        CBU =''.join([str(random.randint(0, 9)) for i in range(22)])
        
        moneda_limpia = obtener_moneda(tipo_cuenta)
        
        ALIAS = cliente_encontrado["Usuario"] + '.bank.' + moneda_limpia

        cliente_encontrado[tipo_cuenta] = {
            "Saldo": 0.0,
            "Datos": (CBU, ALIAS) 
        }
        
        print(f"{tipo_cuenta} creada exitosamente. Saldo inicial: 0.0 {moneda}.")
        print(f"CBU: {CBU} | ALIAS: {ALIAS}")
    
    pausar_y_volver()

def depositar(lista_clientes, dni_actual, monto, tipo_cuenta, moneda):
    """
    Deposita un monto en la cuenta indicada del cliente.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        monto (float): Importe a acreditar (debe ser positivo).
        tipo_cuenta (str): Cuenta destino del depósito.
        moneda (str): Moneda mostrada en pantalla.
    """
    cliente_encontrado = None
    for cliente in lista_clientes:
        if cliente["dni_actual"] == dni_actual:
            cliente_encontrado = cliente

    limpiar_pantalla()
    if cliente_encontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        pausar_y_volver()
        return False
    
    if tipo_cuenta not in cliente_encontrado:
        print(f"El cliente no posee una cuenta en {tipo_cuenta}. Debe crearla primero")
        pausar_y_volver()
        return False
    
    if monto <= 0:
        print("El monto a depositar debe ser mayor a 0")
        pausar_y_volver()
        return False
    
    cliente_encontrado[tipo_cuenta]["Saldo"] += monto
    print(f"Depósito realizado con éxito. Saldo actual: {cliente_encontrado[tipo_cuenta]['Saldo']:.2f} {moneda}")
    
    pausar_y_volver()
    return True

def consultar_saldo(lista_clientes, dni_actual, tipo_cuenta, moneda):
    """
    Muestra el saldo actual de una cuenta del cliente.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        tipo_cuenta (str): Cuenta a consultar.
        moneda (str): Moneda para la impresión del saldo.
    """

    cliente_encontrado = None

    for cliente in lista_clientes:
        if cliente["dni_actual"] == dni_actual:
            cliente_encontrado = cliente

    limpiar_pantalla()
    if cliente_encontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        pausar_y_volver()
        return None
    
    if tipo_cuenta not in cliente_encontrado:
        print(f"El cliente no posee una cuenta en {tipo_cuenta}. Debe crearla primero")
        pausar_y_volver()
        return
      
    print(f"Saldo actual en {tipo_cuenta} ({moneda}): {cliente_encontrado[tipo_cuenta]['Saldo']:.2f} {moneda}")
    
    pausar_y_volver()

def transferir_entre_cuentas(lista_clientes, dni_actual, origen, destino, monto, tasa=1000):
    """
    Pasa fondos entre cuentas del mismo cliente (ARS ↔ USD), aplicando conversión.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        origen (str): Cuenta desde donde se debita.
        destino (str): Cuenta a la que se acredita.
        monto (float): Importe a transferir (debe ser positivo).
        tasa (float): Tipo de cambio ARS por USD usado en la conversión.
    """

    usd_a_ars = lambda usd: usd * tasa
    ars_a_usd = lambda ars: ars / tasa

    cliente = None
    for c in lista_clientes:
        if c.get("dni_actual") == dni_actual:
            cliente = c
    
    limpiar_pantalla()


    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return False


    if origen not in cliente or "Saldo" not in cliente[origen]:
        print(f"La cuenta de origen {origen} no existe o no tiene saldo definido.")
        pausar_y_volver()
        return False
    
    if destino not in cliente or "Saldo" not in cliente[destino]:
        print(f"La cuenta de destino {destino} no existe o no tiene saldo definido.")
        pausar_y_volver()
        return False


    saldo_origen = cliente[origen]["Saldo"]
    if saldo_origen < monto:
        print(f"Saldo insuficiente en la cuenta de origen {origen}. Saldo: {saldo_origen:.2f}")
        pausar_y_volver()
        return False
    
    if monto <= 0:
        print("El monto a transferir debe ser mayor a 0.")
        pausar_y_volver()
        return False

    if origen == "Cuenta en pesos" and destino == "Cuenta en dólares":
        cliente[origen]["Saldo"] -= monto
        monto_acreditado = ars_a_usd(monto)
        cliente[destino]["Saldo"] += monto_acreditado
        print(f"Transferencia exitosa: Se debitaron {monto:.2f} ARS y se acreditaron {monto_acreditado:.2f} USD (Tasa: {tasa}).")

    elif origen == "Cuenta en dólares" and destino == "Cuenta en pesos":
        cliente[origen]["Saldo"] -= monto
        monto_acreditado = usd_a_ars(monto)
        cliente[destino]["Saldo"] += monto_acreditado
        print(f"Transferencia exitosa: Se debitaron {monto:.2f} USD y se acreditaron {monto_acreditado:.2f} ARS (Tasa: {tasa}).")

    else:
        print("Transferencia no válida: ambas cuentas son del mismo tipo.")
        pausar_y_volver()
        return False
    
    pausar_y_volver()
    return True

def registrar_operacion(usuario, tipo_operacion, archivo="operaciones.csv"):
    """
    Anota una operación en un archivo CSV (crea el encabezado si el archivo no existe).

    Args:
        usuario (str): Nombre de usuario asociado a la operación.
        tipo_operacion (str): Descripción breve de la operación.
        archivo (str): Ruta del CSV donde se guardan los movimientos (por defecto, 'operaciones.csv').
    """
    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="UTF8") as f:
            f.write("Tipo de Operación;Usuario;Fecha y Hora\n")

    fecha_hora = time.asctime(time.localtime())

    with open(archivo, "a", encoding="UTF8") as f:
        f.write(tipo_operacion + ";" + usuario + ";" + fecha_hora + "\n")

def obtener_movimientos_usuario(usuario, archivo="operaciones.csv"):
    """
    Devuelve todas las líneas del CSV que corresponden exactamente al usuario indicado.

    Args:
        usuario (str): Usuario a filtrar.
        archivo (str): Ruta del archivo de operaciones.

    Returns:
        list[str]: Líneas ya formateadas, sin el encabezado.
    """
    filas = []
    if not os.path.exists(archivo):
        return filas
    with open(archivo, "r", encoding="utf-8") as f:
        primera = True
        for linea in f:
            if primera:
                primera = False
                continue
            partes = linea.rstrip("\n").split(";")
            if len(partes) >= 3 and partes[1] == usuario:
                filas.append(linea.strip())
    return filas

def historial_cargas_celular(lista_clientes, dni_actual):
    """
    Muestra el historial de cargas de celular del cliente,
    leyendo la información detallada guardada dentro del cliente
    (número, compañía, monto, fecha).

    Args:
        lista_clientes (list): Lista de clientes en memoria.
        dni_actual (int): DNI del cliente autenticado.
    """
    limpiar_pantalla()
    print("===== HISTORIAL DE CARGAS DE CELULAR =====\n")

    cliente = next((c for c in lista_clientes if c["dni_actual"] == dni_actual), None)

    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return

    historial = cliente.get("Historial_celular", [])

    if not historial:
        print("No se encontraron cargas de celular para este usuario.")
    else:
        for registro in historial:
            numero = registro.get("numero", "N/D")
            compania = registro.get("compania", "N/D")
            monto = registro.get("monto", 0.0)
            fecha_hora = registro.get("fecha_hora", "Sin fecha")
            print(f"{fecha_hora} - Número: {numero} - Compañía: {compania} - Monto: {monto:.2f} ARS")

    pausar_y_volver()


def cargar_celular(lista_clientes, dni_actual, monto):
    """
    Acredita una carga de celular, descontando de la cuenta en pesos.
    NO registra en operaciones.csv (eso lo hace el menú general),
    pero guarda el detalle de la carga dentro del cliente para el historial.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        monto (float): Monto a cargar (en ARS).

    Returns:
        bool: True si la carga se realizó con éxito, False en caso contrario.
    """
    cliente = next((c for c in lista_clientes if c["dni_actual"] == dni_actual), None)

    limpiar_pantalla()

    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return False

    if monto <= 0:
        print("El monto debe ser mayor a 0.")
        pausar_y_volver()
        return False

    if "Cuenta en pesos" not in cliente:
        print("Debe tener una cuenta en pesos para realizar una carga de celular.")
        pausar_y_volver()
        return False

    if cliente["Cuenta en pesos"]["Saldo"] < monto:
        print("Saldo insuficiente en la cuenta en pesos.")
        pausar_y_volver()
        return False

    numero_celular = input("Ingrese el número de celular (ej: 11XXXXXXXX): ").strip()

    compania = None
    while compania is None:
        print("\nSeleccione la compañía:")
        print("1. Claro")
        print("2. Movistar")
        print("3. Personal")
        print("4. Tuenti")
        try:
            opcion = int(input("Opción (1-4): "))
        except ValueError:
            print("Opción inválida. Debe ingresar un número entre 1 y 4.")
            time.sleep(1.5)
            limpiar_pantalla()
            continue

        if opcion == 1:
            compania = "Claro"
        elif opcion == 2:
            compania = "Movistar"
        elif opcion == 3:
            compania = "Personal"
        elif opcion == 4:
            compania = "Tuenti"
        else:
            print("Opción inválida. Debe elegir un valor entre 1 y 4.")
            time.sleep(1.5)
            limpiar_pantalla()

    cliente["Cuenta en pesos"]["Saldo"] -= monto

    fecha_hora = time.asctime(time.localtime())
    registro = {
        "numero": numero_celular,
        "compania": compania,
        "monto": monto,
        "fecha_hora": fecha_hora
    }

    if "Historial_celular" not in cliente:
        cliente["Historial_celular"] = []
    cliente["Historial_celular"].append(registro)

    print("\nCarga de celular realizada con éxito.")
    print(f"Número: {numero_celular}")
    print(f"Compañía: {compania}")
    print(f"Monto cargado: {monto:.2f} ARS")
    print(f"Saldo restante en Cuenta en pesos: {cliente['Cuenta en pesos']['Saldo']:.2f} ARS")

    pausar_y_volver()
    return True



def extraer_dinero(lista_clientes, dni_actual, monto, tipo_cuenta, moneda):
    """
    Realiza una extracción desde una cuenta del cliente si hay saldo suficiente.

    Args:
        lista_clientes (list): Lista de clientes.
        dni_actual (INT): DNI del titular. 
        monto (float): Importe a retirar.
        tipo_cuenta (str): Cuenta desde la cual se debita.
        moneda (str): Moneda para mostrar el resultado.

    Returns:
        bool: True si la extracción se realizó con éxito, False en caso contrario.
    """

    cliente = next((c for c in lista_clientes if c["dni_actual"] == dni_actual), None)

    limpiar_pantalla()

    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return False

    if tipo_cuenta not in cliente:
        print(f"No posee una {tipo_cuenta}.")
        pausar_y_volver()
        return False

    if monto <= 0:
        print("El monto debe ser mayor a 0.")
        pausar_y_volver()
        return False

    if cliente[tipo_cuenta]["Saldo"] < monto:
        print("Saldo insuficiente.")
        pausar_y_volver()
        return False

    # Si llegó hasta acá, la extracción es válida
    cliente[tipo_cuenta]["Saldo"] -= monto
    print(f"Extracción exitosa. Saldo restante: {cliente[tipo_cuenta]['Saldo']:.2f} {moneda}")
    pausar_y_volver()
    return True

#MAIN
def main():
    """
    Entrada principal: muestra el menú inicial, gestiona el alta o login
    y luego habilita el menú de operaciones mientras dure la sesión.

    Args:
        None
    """
    lista_clientes = cargar_clientes()
    mostrar_menu = False 
    cliente_actual = None

    limpiar_pantalla()
    print("+---------------------------------------------------------------------+")
    print("| Bienvenido/a al HomeBanking. Elija una opción para comenzar.        |")
    print("+---------------------------------------------------------------------+")

    opcion_main = None
    while opcion_main is None:
        try:
            opcion_main = int(input("1 para iniciar sesión, 2 para crear una cuenta: "))
        except ValueError:
            print("Ingresó un valor no numérico.")
            time.sleep(1.5)

    if opcion_main == 1:
        cliente_actual = iniciar_sesion(lista_clientes)

        if cliente_actual is not None:
            mostrar_menu = True

    elif opcion_main == 2:
        nuevo_cliente = registrar_usuario(lista_clientes)
        if nuevo_cliente is not None:
            lista_clientes.append(nuevo_cliente)
            guardar_clientes(lista_clientes)
            cliente_actual = nuevo_cliente
            print("Cuenta creada e iniciada sesión automáticamente.")
            mostrar_menu = True
        else:
            print("Finalizando... Inicie sesión en el próximo intento.")
    else:
        print("Opción inválida en el menú principal.")
        time.sleep(1.5)

    if mostrar_menu and cliente_actual:
        dni_actual = cliente_actual["dni_actual"]
        continuar_operaciones = True
        while continuar_operaciones:
            limpiar_pantalla()
            print("\n+-------------------------MENÚ DE OPERACIONES-------------------------+")
            print(f"| Bienvenido/a | Usuario: {cliente_actual['Usuario']} | DNI: {cliente_actual['dni_actual']}")
            print("+---------------------------------------------------------------------+")
            print("| 1. Crear una cuenta en pesos (ARS)                                  |")
            print("| 2. Depositar pesos (ARS)                                            |")
            print("| 3. Consultar saldo en pesos (ARS)                                   |")
            print("| 4. Crear una cuenta en dólares (USD)                                |")
            print("| 5. Depositar dólares (USD)                                          |")
            print("| 6. Consultar saldo en dólares (USD)                                 |")
            print("| 7. Transferir entre sus cuentas (ARS <-> USD)                       |")
            print("| 8. Consultar movimientos del sistema                                |")
            print("| 9. Extraer dinero                                                   |")
            print("| 10. Cargar Celular                                                  |")
            print("| 11. Historial de Cargas de Celular                                  |")
            print("| 12. Salir                                                           |")
            print("+---------------------------------------------------------------------+")

            try:
                opcion_cuentas = int(input("Ingrese un número del 1 al 12 según la operación que desee realizar: "))
            except ValueError:
                print("Opción inválida, ingrese solo números.")
                time.sleep(1.5)
                continue

            if opcion_cuentas == 1:
                crear_cuenta(lista_clientes, dni_actual, "Cuenta en pesos", "ARS")
                registrar_operacion(cliente_actual["Usuario"], "Creación de cuenta")
                guardar_clientes(lista_clientes)

            elif opcion_cuentas == 2:
                if "Cuenta en pesos" in cliente_actual:
                    try:
                        monto = float(input("Ingrese el monto a depositar en pesos: "))
                        if depositar(lista_clientes, dni_actual, monto, "Cuenta en pesos", "ARS"):
                            registrar_operacion(cliente_actual["Usuario"], "Depositar pesos")
                            guardar_clientes(lista_clientes)
                    except ValueError:
                        print("Monto inválido. Ingrese un valor numérico.")
                        pausar_y_volver()
                else:
                    limpiar_pantalla()
                    print("No posee una Cuenta en pesos. Debe crearla primero para depositar dinero.")
                    pausar_y_volver()

            elif opcion_cuentas == 3:
                consultar_saldo(lista_clientes, dni_actual, "Cuenta en pesos", "ARS")
                registrar_operacion(cliente_actual["Usuario"], "Consultar saldo")

            elif opcion_cuentas == 4:
                crear_cuenta(lista_clientes, dni_actual, "Cuenta en dólares", "USD")
                registrar_operacion(cliente_actual["Usuario"], "Crear cuenta en dolares")
                guardar_clientes(lista_clientes)

            elif opcion_cuentas == 5:
                if "Cuenta en dólares" in cliente_actual:
                    try:
                        monto = float(input("Ingrese el monto a depositar en dólares: "))
                        if depositar(lista_clientes, dni_actual, monto, "Cuenta en dólares", "USD"):
                            registrar_operacion(cliente_actual["Usuario"], "Depositar dolares")
                            guardar_clientes(lista_clientes)
                    except ValueError:
                        print("Monto inválido. Ingrese un valor numérico.")
                        pausar_y_volver()
                else:
                    limpiar_pantalla()
                    print("No posee una Cuenta en dólares. Debe crearla primero para depositar dinero.")
                    pausar_y_volver()
            
            elif opcion_cuentas == 6:
                consultar_saldo(lista_clientes, dni_actual, "Cuenta en dólares", "USD")
                registrar_operacion(cliente_actual["Usuario"], "Consultar saldo")

            elif opcion_cuentas == 7:
                limpiar_pantalla()

                tiene_pesos = "Cuenta en pesos" in cliente_actual
                tiene_dolares = "Cuenta en dólares" in cliente_actual

                if not tiene_pesos and not tiene_dolares:
                    print("No posee ninguna cuenta. Cree una cuenta en pesos o dólares antes de transferir.")
                    pausar_y_volver()
                    continue

                if not tiene_pesos:
                    print("No posee Cuenta en pesos. Cree una antes de transferir ARS ↔ USD.")
                    pausar_y_volver()
                    continue

                if not tiene_dolares:
                    print("No posee Cuenta en dólares. Cree una antes de transferir ARS ↔ USD.")
                    pausar_y_volver()
                    continue

                try:
                    monto = float(input("Ingrese el monto a transferir: "))
                except ValueError:
                    print("Monto u opción inválido. Ingrese un valor numérico.")
                    pausar_y_volver()
                    continue

                if monto <= 0:
                    print("El monto debe ser mayor a 0.")
                    pausar_y_volver()
                    continue

                print("\nSeleccione tipo de transferencia:")
                print("1. Pesos (ARS) -> Dólares (USD)")
                print("2. Dólares (USD) -> Pesos (ARS)")

                try:
                    tipo = int(input("Opción: "))
                except ValueError:
                    print("Opción inválida.")
                    pausar_y_volver()
                    continue

                exito_transferencia = False
                desc_operacion = ""

                if tipo == 1:
                    exito_transferencia = transferir_entre_cuentas(lista_clientes, dni_actual, "Cuenta en pesos", "Cuenta en dólares", monto)
                    desc_operacion = "Transferencia ARS a USD"

                elif tipo == 2:
                    exito_transferencia = transferir_entre_cuentas(lista_clientes, dni_actual, "Cuenta en dólares", "Cuenta en pesos", monto)
                    desc_operacion = "Transferencia USD a ARS"

                else:
                    print("Opción de transferencia inválida.")
                    pausar_y_volver()
                    continue

                if exito_transferencia:
                    registrar_operacion(cliente_actual["Usuario"], desc_operacion)
                    guardar_clientes(lista_clientes)
        
            elif opcion_cuentas == 8:
                movimientos = obtener_movimientos_usuario(cliente_actual["Usuario"], "operaciones.csv")
                print(f"\nMovimientos del usuario {cliente_actual['Usuario']}:")
                if movimientos:
                    for linea in movimientos:
                        print(linea)
                else:
                    print("No se encontraron movimientos para este usuario.")
                pausar_y_volver()

            elif opcion_cuentas == 9:
                try:
                    tipo = int(input("Seleccione cuenta: 1-Pesos / 2-Dólares: "))
                except ValueError:
                    print("Opción inválida. Debe ingresar 1 o 2.")
                    pausar_y_volver()
                    continue

                if tipo not in (1, 2):
                    print("Opción inválida. Debe seleccionar 1-Pesos o 2-Dólares.")
                    pausar_y_volver()
                    continue

                try:
                    monto = float(input("Ingrese el monto a extraer: "))
                except ValueError:
                    print("Monto inválido. Ingrese un número positivo.")
                    pausar_y_volver()
                    continue

                if monto <= 0:
                    print("El monto debe ser mayor que 0.")
                    pausar_y_volver()
                    continue

                exito_extraccion = False
                if tipo == 1:
                    exito_extraccion = extraer_dinero(lista_clientes, dni_actual, monto, "Cuenta en pesos", "ARS")
                else:
                    exito_extraccion = extraer_dinero(lista_clientes, dni_actual, monto, "Cuenta en dólares", "USD")

                if exito_extraccion:
                    registrar_operacion(cliente_actual["Usuario"], "Extracción de dinero")
                    guardar_clientes(lista_clientes)

            elif opcion_cuentas == 10:
                try:
                    monto = float(input("Ingrese el monto que desea cargar a su celular: "))
                    if monto <= 0:
                        print("El monto debe ser mayor que 0.")
                        pausar_y_volver()
                        continue
                except ValueError:
                    print("Monto inválido. Ingrese un número positivo.")
                    pausar_y_volver()
                    continue

                exito_carga = cargar_celular(lista_clientes, dni_actual, monto)
                if exito_carga:
                    # En operaciones.csv solo se guarda "Carga Celular"
                    registrar_operacion(cliente_actual["Usuario"], "Carga Celular")
                    guardar_clientes(lista_clientes)


            elif opcion_cuentas == 11:
                historial_cargas_celular(lista_clientes, dni_actual)

            elif opcion_cuentas == 12:
                print("Sesión finalizada. Muchas gracias por usar nuestro HomeBanking.")
                registrar_operacion(cliente_actual["Usuario"], "Cierre de sesion")
                guardar_clientes(lista_clientes)
                continuar_operaciones = False

            else:
                print("Opción inválida en el menú de operaciones.")
                time.sleep(1.5)

main()