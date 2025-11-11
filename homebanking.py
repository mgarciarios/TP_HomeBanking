"""
HomeBanking básico con registro, login, cuentas y operaciones simples.
"""
import random
import os
import time
import json
from persistencia import guardarClientes, cargarClientes

def limpiarPantalla():
    """
    Función estética para limpiar la terminal y mejorar la visualización.
    La primera condición es para sistemas Windows ('nt') y la segunda para MacOs y Linux.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pausar_y_volver():
    """Pausa la ejecución y pide confirmación para volver al menú principal."""
    input("\nPresione ENTER para volver al menú de operaciones...")
    limpiarPantalla()

def registrarUsuario(listaClientes):
    
    """
    Registra un nuevo cliente validando dni_actual, unicidad de usuario y requisitos de contraseña.

    Solicita al usuario ingresar su dni_actual. Si ya existe, termina el proceso.
    Si es nuevo, solicita un nombre de usuario (verifica que no esté repetido)
    y una contraseña (entre 8 y 12 caracteres, con confirmación).

    Args:
        listaClientes (list): Lista actual de clientes (diccionarios) para verificar duplicados.

    Returns:
        dict: Un diccionario con las claves dni_actual, Usuario y Contraseña del nuevo cliente si el registro es exitoso.
        None: Si el dni_actual ya estaba registrado.
    """ 

    nuevoCliente = {}

    # dni_actual
    limpiarPantalla()
    dni_actual = int(input("Ingrese su dni, sin puntos (ej: XXXXXXXX): "))

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

    # Contraseña
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
    Verifica dni_actual, usuario y contraseña para iniciar sesión con reintentos.

    Args:
        lista (list): Una lista de diccionarios, donde cada diccionario representa a un cliente y debe contener las claves dni_actual, Usuario, y Contraseña.

    Returns:
        bool: True si el inicio de sesión es exitoso, False si el usuario
              decide no reintentar después de un fallo.
    """

    while True:
        limpiarPantalla()
        dni_actual = int(input("Ingrese su dni sin puntos (ej: XXXXXXXX): "))
        dni_actual_encontrado = False
        
        for cliente in lista:
            if cliente["dni_actual"] == dni_actual:
                dni_actual_encontrado = True
                limpiarPantalla()
                usuario = input("Ingrese su usuario: ")
                
                if cliente["Usuario"] == usuario:
                    limpiarPantalla()
                    contraseña = input("Ingrese su contraseña: ")
                    
                    if cliente["Contraseña"] == contraseña:
                        print("Ingreso exitoso. Bienvenido/a.")
                        return cliente 
                    else:
                        break
                else:
                    break 
        
        print("Algún dato se ingresó de manera incorrecta. DNI, Usuario o Contraseña no coinciden.")
        
        continuar = input("¿Desea intentar ingresar nuevamente? (S/N): ").upper()
        if continuar == 'N':
            print("Ha salido del sistema exitosamente.")
            return None


def sumarUsuarioALaBD(cliente, listaClientes):
    """
    Agrega un diccionario de cliente a una lista si no existe previamente.
    """
    if cliente not in listaClientes:
        listaClientes.append(cliente)
    return listaClientes


def crearCuenta(listaClientes, dni_actual, tipoCuenta, moneda):

    """
    Intenta crear una nueva cuenta con saldo 0.0 para un cliente existente.
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
    Suma un monto específico al saldo de una cuenta de cliente existente.
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
    Muestra el saldo de una cuenta específica de un cliente si existe.
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
    Transfiere un monto entre las cuentas en pesos y dólares de un cliente.
    """

    usd_a_ars = lambda usd: usd * tasa
    ars_a_usd = lambda ars: ars / tasa

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
    Registra una operación realizada por un cliente en un archivo CSV.
    Si el archivo no existe, lo crea y escribe el encabezado. 
    Cada registro contiene: tipo_operacion;usuario;fecha_hora
       Args: usuario, tipo_operacion, archivo
       Returns: operaciones.csv con tipo_operacion; usuario; fecha_hora
    """
    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="UTF8") as f:
            f.write("Tipo de Operación;Usuario;Fecha y Hora\n")

    fecha_hora = time.asctime(time.localtime())

    with open(archivo, "a", encoding="UTF8") as f:
        f.write(tipo_operacion + ";" + usuario + ";" + fecha_hora + "\n")

def verRegistros(listaClientes):
    """
    Muestra todos los registros de los clientes: nombre, DNI y saldos de sus cuentas.
    Solo para revisión o administración.
    """
    limpiarPantalla()
    print("=== REGISTROS DE CLIENTES ===")
    if not listaClientes:
        print("No hay clientes registrados.")
    else:
        for cliente in listaClientes:
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
    Carga saldo en la SUBE del cliente, debitando el monto desde la cuenta en pesos.
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

    if "Cuenta en pesos" not in cliente:
        print("Debe tener una cuenta en pesos para cargar la SUBE.")
        pausar_y_volver()
        return

    # Aca vamos a cerar la SUBE en caso de no tenerla
    if "SUBE" not in cliente:
        cliente["SUBE"] = {
            "Saldo": 0.0,
            "Número SUBE": str(random.randint(1000,9999)) + "-" + str(random.randint(1000,9999))
        }

    if cliente["Cuenta en pesos"]["Saldo"] < monto:
        print("Saldo insuficiente en la cuenta en pesos.")
        pausar_y_volver()
        return

    cliente["Cuenta en pesos"]["Saldo"] -= monto
    cliente["SUBE"]["Saldo"] += monto

    print(f"Se cargaron {monto:.2f} ARS a la SUBE.")
    print(f"Saldo actual SUBE: {cliente['SUBE']['Saldo']:.2f} ARS")
    registrarOperacion(cliente["Usuario"], f"Carga SUBE {monto:.2f} ARS")
    guardarClientes(listaClientes)
    pausar_y_volver()

def extraerDinero(listaClientes, dni_actual, monto, tipoCuenta, moneda):
    """
    Permite retirar dinero de una cuenta (en pesos o dólares).
    """
    cliente = None
    for i in listaClientes:
        if i["dni_actual"] == dni_actual:
            cliente = i

    limpiarPantalla()
    if cliente is None:
        print("Cliente no encontrado.")
        pausar_y_volver()
        return

    if tipoCuenta not in cliente:
        print(f"No posee una {tipoCuenta}.")
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
            sumarUsuarioALaBD(nuevoCliente, listaClientes)
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
            print("| 10. Cargar SUBE                                                      |")
            print("| 11. Ver registros de clientes                                        |")
            print("| 12. Salir                                                            |")
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
                try:
                    monto = float(input("Ingrese el monto a depositar en dólares: "))
                    depositar(listaClientes, dni_actual, monto, "Cuenta en dólares", "USD")
                    guardarClientes(listaClientes)
                    monto = float(input("Ingrese el monto a transferir: "))

                    print("\nSeleccione tipo de transferencia:")
                    print("1. Pesos (ARS) -> Dólares (USD)")
                    print("2. Dólares (USD) -> Pesos (ARS)")
                    tipo = int(input("Opción: "))

                    if tipo == 1:
                        transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en pesos", "Cuenta en dólares", monto)
                        registrarOperacion(cliente_actual["Usuario"], "Comprar dolares")
                    elif tipo == 2:
                        transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en dólares", "Cuenta en pesos", monto)
                        registrarOperacion(cliente_actual["Usuario"], "Comprar pesos")
                    else:
                        print("Opción de transferencia inválida.")
                        pausar_y_volver()
                except ValueError:
                    print("Monto/Opción inválida. Ingrese un valor numérico.")
                    pausar_y_volver()


            elif opcionCuentas == 8:
                try:
                    with open("operaciones.csv", "r", encoding="utf-8") as archivo:
                        print(f"\nMovimientos del usuario {cliente_actual['Usuario']}:")
                        encontrados = False
                        for linea in archivo:
                            if cliente_actual['Usuario'] in linea:
                                print(linea.strip())
                                encontrados = True
                        if not encontrados:
                            print("No se encontraron movimientos para este usuario.")
                except FileNotFoundError:
                    print("No hay operaciones registradas todavía.")
                
                pausar_y_volver()

            elif opcionCuentas == 9:
                DNI = int(input("Ingrese su DNI: "))
                tipo = int(input("Seleccione cuenta: 1-Pesos / 2-Dólares: "))
                monto = float(input("Ingrese el monto a extraer: "))
                if tipo == 1:
                    extraerDinero(listaClientes, DNI, monto, "Cuenta en pesos", "ARS")
                elif tipo == 2:
                    extraerDinero(listaClientes, DNI, monto, "Cuenta en dólares", "USD")
                else:
                    print("Opción inválida.") 

            elif opcionCuentas == 10:
                DNI = int(input("Ingrese su DNI: "))
                monto = float(input("Ingrese el monto a cargar en la SUBE: "))
                cargarSube(listaClientes, DNI, monto)   

            elif opcionCuentas == 11:
                verRegistros(listaClientes)

            elif opcionCuentas == 12:
                print("Sesión finalizada. Muchas gracias por usar nuestro HomeBanking.")
                registrarOperacion(cliente_actual["Usuario"], "Cierre de sesion")
                guardarClientes(listaClientes)
                continuarOperaciones = False

            else:
                print("Opción inválida en el menú de operaciones.")
                time.sleep(1.5)

main()