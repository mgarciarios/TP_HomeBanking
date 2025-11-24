"""
HomeBanking básico con registro, login, cuentas y operaciones simples.
"""
import random
import os
import time
import json
from persistencia import guardarClientes, cargarClientes

def pedir_dni():
    while True:
        try:
            return int(input("Ingrese su DNI sin puntos (ej: 12345678): "))
        except ValueError:
            print("DNI inválido. Solo números.")
            time.sleep(1.0)

def limpiarPantalla():
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
    input("\nPresione ENTER para volver al menú de operaciones...")
    limpiarPantalla()

def registrarUsuario(listaClientes):
    """
    Registra un cliente nuevo validando que el DNI no exista, que el usuario no se repita
    y que la contraseña cumpla con los requisitos básicos.

    Args:
        listaClientes (list): Lista de clientes persistidos, cada uno como diccionario.

    Returns:
        dict | None: El cliente creado si todo salió bien; None si el DNI ya estaba registrado.
    """ 

    nuevoCliente = {}

    # dni_actual
    limpiarPantalla()
    dni_actual = pedir_dni()

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            print("El DNI ya está registrado. Por favor, inicie sesión.")
            return 

    nuevoCliente["dni_actual"] = dni_actual

    # Usuario
    limpiarPantalla()
    usuario = input("Ingrese su usuario (se recomienda la primer letra del nombre y su apellido): ")    
    
    existeCliente = True
    while existeCliente:
        existeCliente = False
        for cliente in listaClientes:
            if cliente["Usuario"] == usuario:
                existeCliente = True
                print("Ese nombre de usuario ya fue registrado")
                usuario = input("Ingrese otro usuario: ")
        
    nuevoCliente["Usuario"] = usuario

    while True:
        limpiarPantalla()
        contraseña1 = input("Ingrese una contraseña (debe tener entre 8 y 12 caracteres, contener una mayúscula y un número): ")

        if not (8 <= len(contraseña1) <= 12):
            print("Error: La contraseña debe tener entre 8 y 12 caracteres.")
            time.sleep(1.5)
        else:
            tiene_mayuscula = False
            tiene_numero = False

            for caracter in contraseña1:
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
                limpiarPantalla()
                contraseña2 = input("Repita la contraseña: ")
                if contraseña1 == contraseña2:
                    nuevoCliente["Contraseña"] = contraseña1
                    print("¡Usuario registrado exitosamente!")
                    return nuevoCliente
                else:
                    print("Las contraseñas no coinciden. Intente de nuevo.")
                    time.sleep(1.5)

def iniciarSesion(lista):
    """
    Inicia sesión pidiendo DNI, usuario y contraseña. Permite reintentos.

    Args:
        lista (list): Lista de clientes (diccionarios) con 'dni_actual', 'Usuario' y 'Contraseña'.

    Returns:
        dict | None: El cliente autenticado si los datos son correctos; None si el usuario decide salir.
    """
    while True:
        limpiarPantalla()
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

def crearCuenta(listaClientes, dni_actual, tipoCuenta, moneda):
    """
    Crea una cuenta para el cliente si no la tiene ya, con saldo inicial 0.0.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (int): DNI del titular de la cuenta.
        tipoCuenta (str): Nombre de la cuenta a crear (ej.: "Cuenta en pesos").
        moneda (str): Código de moneda para mostrar en pantalla (ej.: "ARS", "USD").

    Returns:
        dict | None: El cliente actualizado si se creó; None si no se encontró el cliente.
    """    
    obtener_moneda = lambda tipo_cuenta: tipo_cuenta.split(' ')[2].replace('dólares', 'dolares')

    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual: 
            clienteEncontrado = cliente
    
    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta in clienteEncontrado:
        print(f"El cliente ya posee una cuenta en {tipoCuenta}.")

    else:
        CBU =''.join([str(random.randint(0, 9)) for i in range(22)])
        
        moneda_limpia = obtener_moneda(tipoCuenta)
        
        ALIAS = clienteEncontrado["Usuario"] + '.bank.' + moneda_limpia

        clienteEncontrado[tipoCuenta] = {
            "Saldo": 0.0,
            "Datos": (CBU, ALIAS) 
        }
        
        print(f"{tipoCuenta} creada exitosamente. Saldo inicial: 0.0 {moneda}.")
        print(f"CBU: {CBU} | ALIAS: {ALIAS}")
    
    pausar_y_volver()

def depositar(listaClientes, dni_actual, monto, tipoCuenta, moneda):
    """
    Deposita un monto en la cuenta indicada del cliente.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        monto (float): Importe a acreditar (debe ser positivo).
        tipoCuenta (str): Cuenta destino del depósito.
        moneda (str): Moneda mostrada en pantalla.
    """
    clienteEncontrado = None
    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            clienteEncontrado = cliente

    limpiarPantalla()
    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        pausar_y_volver()
        return None
    
    if tipoCuenta not in clienteEncontrado:
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        pausar_y_volver()
        return
    
    if monto <= 0:
        print("El monto a depositar debe ser mayor a 0")
        pausar_y_volver()
        return
    
    clienteEncontrado[tipoCuenta]["Saldo"] += monto
    print(f"Depósito realizado con éxito. Saldo actual: {clienteEncontrado[tipoCuenta]['Saldo']:.2f} {moneda}")
    
    pausar_y_volver()

def consultarSaldo(listaClientes, dni_actual, tipoCuenta, moneda):
    """
    Muestra el saldo actual de una cuenta del cliente.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        tipoCuenta (str): Cuenta a consultar.
        moneda (str): Moneda para la impresión del saldo.
    """

    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            clienteEncontrado = cliente

    limpiarPantalla()
    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        pausar_y_volver()
        return None
    
    if tipoCuenta not in clienteEncontrado:
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        pausar_y_volver()
        return
      
    print(f"Saldo actual en {tipoCuenta} ({moneda}): {clienteEncontrado[tipoCuenta]['Saldo']:.2f} {moneda}")
    
    pausar_y_volver()

def transferirEntreCuentas(listaClientes, dni_actual, origen, destino, monto, tasa=1000):
    """
    Pasa fondos entre cuentas del mismo cliente (ARS ↔ USD), aplicando conversión.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        origen (str): Cuenta desde donde se debita.
        destino (str): Cuenta a la que se acredita.
        monto (float): Importe a transferir (debe ser positivo).
        tasa (float): Tipo de cambio ARS por USD usado en la conversión.
    """

    # conversiones
    usd_a_ars = lambda usd: usd * tasa
    ars_a_usd = lambda ars: ars / tasa

    # buscar clientes
    cliente = None
    for c in listaClientes:
        if c.get("dni_actual") == dni_actual:
            cliente = c
    
    limpiarPantalla()


    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return


    if origen not in cliente or "Saldo" not in cliente[origen]:
        print(f"La cuenta de origen {origen} no existe o no tiene saldo definido.")
        pausar_y_volver()
        return None
    
    if destino not in cliente or "Saldo" not in cliente[destino]:
        print(f"La cuenta de destino {destino} no existe o no tiene saldo definido.")
        pausar_y_volver()
        return None


    saldo_origen = cliente[origen]["Saldo"]
    if saldo_origen < monto:
        print(f"Saldo insuficiente en la cuenta de origen {origen}. Saldo: {saldo_origen:.2f}")
        pausar_y_volver()
        return None
    
    if monto <= 0:
        print("El monto a transferir debe ser mayor a 0.")
        pausar_y_volver()
        return

    # para actualizar los saldos
    cliente[origen]["Saldo"] = saldo_origen - monto

    if origen == "Cuenta en pesos" and destino == "Cuenta en dólares":
        monto_acreditado = ars_a_usd(monto)
        cliente[destino]["Saldo"] += monto_acreditado
        print(f"Transferencia exitosa: Se debitaron {monto:.2f} ARS y se acreditaron {monto_acreditado:.2f} USD (Tasa: {tasa}).")

    elif origen == "Cuenta en dólares" and destino == "Cuenta en pesos":
        monto_acreditado = usd_a_ars(monto)
        cliente[destino]["Saldo"] += monto_acreditado
        print(f"Transferencia exitosa: Se debitaron {monto:.2f} USD y se acreditaron {monto_acreditado:.2f} ARS (Tasa: {tasa}).")

    else:

        cliente[origen]["Saldo"] += monto 
        print("Transferencia no válida (origen y destino son el mismo tipo de cuenta).")
    
    pausar_y_volver()

def registrarOperacion(usuario, tipo_operacion, archivo="operaciones.csv"):
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

def historial_sube(listaClientes, dni_actual):
    """
    Muestra únicamente los datos y saldos del cliente autenticado.

    Args:
        listaClientes (list): Lista de clientes en memoria.
        dni_actual (int): DNI del cliente autenticado.
    """
    limpiarPantalla()
    cliente = None
    for c in listaClientes:
        if c.get("dni_actual") == dni_actual:
            cliente = c
            break

    print("=== HISTORIAL CARGA SUBE ===")
    if not cliente:
        print("No se encontró el cliente en memoria.")
        pausar_y_volver()
        return

    print("\n-----------------------------")
    print(f"Usuario: {cliente.get('Usuario', 'No definido')}")
    print(f"DNI: {cliente.get('dni_actual', 'No definido')}")
    if "Cuenta en pesos" in cliente:
        print(f"Cuenta en pesos: {cliente['Cuenta en pesos']['Saldo']:.2f} ARS")
    if "Cuenta en dólares" in cliente:
        print(f"Cuenta en dólares: {cliente['Cuenta en dólares']['Saldo']:.2f} USD")
    if "SUBE" in cliente:
        print(f"Saldo SUBE: {cliente['SUBE']['Saldo']:.2f} ARS")
    print("\n-----------------------------")
    pausar_y_volver()


def cargarSube(listaClientes, dni_actual, monto):
    """
    Acredita saldo en la SUBE del cliente, descontando de su cuenta en pesos.
    Si no existe la SUBE, la crea con un número simple.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (int): DNI del titular.
        monto (float): Monto a cargar (en ARS).
    """
    cliente = None
    for c in listaClientes:
        if c["dni_actual"] == dni_actual:
            cliente = c

    limpiarPantalla()

    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return

    if monto <= 0:
        print("El monto debe ser mayor a 0.")
        pausar_y_volver()
        return

    if "Cuenta en pesos" not in cliente:
        print("Debe tener una cuenta en pesos para cargar la SUBE.")
        pausar_y_volver()
        return

    if cliente["Cuenta en pesos"]["Saldo"] < monto:
        print("Saldo insuficiente.")
        pausar_y_volver()
        return

    if "SUBE" not in cliente:
        cliente["SUBE"] = {
            "Saldo": 0.0,
            "Número SUBE": str(random.randint(1000,9999)) + "-" + str(random.randint(1000,9999))
        }

    cliente["Cuenta en pesos"]["Saldo"] -= monto
    cliente["SUBE"]["Saldo"] += monto

    print(f"Carga exitosa. Saldo SUBE: {cliente['SUBE']['Saldo']:.2f} ARS")
    registrarOperacion(cliente["Usuario"], f"Carga SUBE {monto:.2f} ARS")
    guardarClientes(listaClientes)
    pausar_y_volver()

def extraerDinero(listaClientes, dni_actual, monto, tipoCuenta, moneda):
    """
    Realiza una extracción desde una cuenta del cliente si hay saldo suficiente.

    Args:
        listaClientes (list): Lista de clientes.
        dni_actual (INT): DNI del titular. 
        monto (float): Importe a retirar.
        tipoCuenta (str): Cuenta desde la cual se debita.
        moneda (str): Moneda para mostrar el resultado.
    """

    cliente = next((c for c in listaClientes if c["dni_actual"] == dni_actual), None)

    limpiarPantalla()

    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return

    if tipoCuenta not in cliente:
        print(f"No posee una {tipoCuenta}.")
        pausar_y_volver()
        return

    if monto <= 0:
        print("El monto debe ser mayor a 0.")
        pausar_y_volver()
        return

    if cliente[tipoCuenta]["Saldo"] < monto:
        print("Saldo insuficiente.")
        pausar_y_volver()
        return

    cliente[tipoCuenta]["Saldo"] -= monto
    print(f"Extracción exitosa. Saldo restante: {cliente[tipoCuenta]['Saldo']:.2f} {moneda}")
    registrarOperacion(cliente["Usuario"], f"Extracción de {monto:.2f} {moneda}")
    guardarClientes(listaClientes)
    pausar_y_volver()

#MAIN
def main():
    """
    Entrada principal: muestra el menú inicial, gestiona el alta o login
    y luego habilita el menú de operaciones mientras dure la sesión.

    Args:
        None
    """
    listaClientes = cargarClientes()
    mostrar_menu = False 
    cliente_actual = None

    limpiarPantalla()
    print("+---------------------------------------------------------------------+")
    print("| Bienvenido/a al HomeBanking. Elija una opción para comenzar.        |")
    print("+---------------------------------------------------------------------+")

    try:
        opcionMain = int(input("1 para iniciar sesión, 2 para crear una cuenta: "))
    except ValueError:
        print("Ingresó un valor no numérico.")
        time.sleep(1.5)
        exit()

    if opcionMain == 1:
        cliente_actual = iniciarSesion(listaClientes)

        if cliente_actual is not None:
            mostrar_menu = True

    elif opcionMain == 2:
        nuevoCliente = registrarUsuario(listaClientes)
        if nuevoCliente is not None:
            listaClientes.append(nuevoCliente)
            guardarClientes(listaClientes)
            cliente_actual = nuevoCliente
            print("Cuenta creada e iniciada sesión automáticamente.")
            mostrar_menu = True
        else:
            print("Finalizando... Inicie sesión en el próximo intento.")
    else:
        print("Opción inválida en el menú principal.")
        time.sleep(1.5)

    if mostrar_menu and cliente_actual:
        dni_actual = cliente_actual["dni_actual"]
        continuarOperaciones = True
        while continuarOperaciones:
            limpiarPantalla()
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
            print("| 10. Cargar SUBE                                                     |")
            print("| 11. Historial carga sube                                            |")
            print("| 12. Salir                                                           |")
            print("+---------------------------------------------------------------------+")

            try:
                opcionCuentas = int(input("Ingrese un número del 1 al 12 según la operación que desee realizar: "))
            except ValueError:
                print("Opción inválida, ingrese solo números.")
                time.sleep(1.5)
                continue

            if opcionCuentas == 1:
                crearCuenta(listaClientes, dni_actual, "Cuenta en pesos", "ARS")
                registrarOperacion(cliente_actual["Usuario"], "Creación de cuenta")

            elif opcionCuentas == 2:
                if "Cuenta en pesos" in cliente_actual:
                    try:
                        monto = float(input("Ingrese el monto a depositar en pesos: "))
                        depositar(listaClientes, dni_actual, monto, "Cuenta en pesos", "ARS")
                        registrarOperacion(cliente_actual["Usuario"], "Depositar pesos")
                    except ValueError:
                        print("Monto inválido. Ingrese un valor numérico.")
                        pausar_y_volver()
                else:
                    limpiarPantalla()
                    print("No posee una Cuenta en pesos. Debe crearla primero para depositar dinero.")
                    pausar_y_volver()

            elif opcionCuentas == 3:
                consultarSaldo(listaClientes, dni_actual, "Cuenta en pesos", "ARS")
                registrarOperacion(cliente_actual["Usuario"], "Consultar saldo")

            elif opcionCuentas == 4:
                crearCuenta(listaClientes, dni_actual, "Cuenta en dólares", "USD")
                registrarOperacion(cliente_actual["Usuario"], "Crear cuenta en dolares")
                guardarClientes(listaClientes)

            elif opcionCuentas == 5:
                if "Cuenta en dólares" in cliente_actual:
                    try:
                        monto = float(input("Ingrese el monto a depositar en dólares: "))
                        depositar(listaClientes, dni_actual, monto, "Cuenta en dólares", "USD")
                        registrarOperacion(cliente_actual["Usuario"], "Depositar dolares")
                    except ValueError:
                        print("Monto inválido. Ingrese un valor numérico.")
                        pausar_y_volver()
                else:
                    limpiarPantalla()
                    print("No posee una Cuenta en dólares. Debe crearla primero para depositar dinero.")
                    pausar_y_volver()
            
            elif opcionCuentas == 6:
                consultarSaldo(listaClientes, dni_actual, "Cuenta en dólares", "USD")
                registrarOperacion(cliente_actual["Usuario"], "Consultar saldo")

            elif opcionCuentas == 7:
                limpiarPantalla()

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
                    monto = float(input("Ingrese el monto a depositar en dólares: "))
                
                except ValueError:
                    print("Monto/Opción inválida. Ingrese un valor numérico.")
                    pausar_y_volver()

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
                    
                    if tipo == 1:
                        transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en pesos", "Cuenta en dólares", monto)
                        registrarOperacion(cliente_actual["Usuario"], "Transferencia ARS a USD")

                    elif tipo == 2:
                        transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en dólares", "Cuenta en pesos", monto)
                        registrarOperacion(cliente_actual["Usuario"], "Transferencia USD a ARS")

                    else:
                        print("Opción de transferencia inválida.")
                        pausar_y_volver()
                        continue

                    guardarClientes(listaClientes)
                    

            elif opcionCuentas == 8:
                movimientos = obtener_movimientos_usuario(cliente_actual["Usuario"], "operaciones.csv")
                print(f"\nMovimientos del usuario {cliente_actual['Usuario']}:")
                if movimientos:
                    for linea in movimientos:
                        print(linea)
                else:
                    print("No se encontraron movimientos para este usuario.")
                pausar_y_volver()

            elif opcionCuentas == 9:
                tipo = int(input("Seleccione cuenta: 1-Pesos / 2-Dólares: "))
                monto = float(input("Ingrese el monto a extraer: "))
                if tipo == 1:
                    extraerDinero(listaClientes, dni_actual, monto, "Cuenta en pesos", "ARS")
                elif tipo == 2:
                    extraerDinero(listaClientes, dni_actual, monto, "Cuenta en dólares", "USD")
                else:
                    print("Opción inválida.") 

            elif opcionCuentas == 10:
                try:
                    monto = float(input("Ingrese el monto a cargar en la SUBE: "))
                    if monto <= 0:
                        print("El monto debe ser mayor que 0.")
                        pausar_y_volver()
                        continue

                except ValueError:
                    print("Monto inválido. Ingrese un número positivo.")
                    pausar_y_volver()
                    continue

                cargarSube(listaClientes, dni_actual, monto) 
                registrarOperacion(cliente_actual["Usuario"], f"Carga SUBE {monto:.2f} ARS")  

            elif opcionCuentas == 11:
                historial_sube(listaClientes, dni_actual)


            elif opcionCuentas == 12:
                print("Sesión finalizada. Muchas gracias por usar nuestro HomeBanking.")
                registrarOperacion(cliente_actual["Usuario"], "Cierre de sesion")
                guardarClientes(listaClientes)
                continuarOperaciones = False

            else:
                print("Opción inválida en el menú de operaciones.")
                time.sleep(1.5)

main()
