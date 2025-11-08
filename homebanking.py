"""
HomeBanking básico con registro, login, cuentas y operaciones simples.
"""
import random

import os
import time

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

    #dni_actual
    dni_actual = int(input("Ingrese su dni_actual, sin puntos: XXXXXXXX "))

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            print("El usuario ya esta registrado, inicie sesión. ")
            return  

    nuevoCliente["dni_actual"] = dni_actual

    #Usuario
    usuario = input("Ingrese su usuario, se recomienda la primer letra del nombre y su apellido: ")    
    
    existeCliente = True
    while existeCliente:
        existeCliente = False
        for cliente in listaClientes:
            if cliente["Usuario"] == usuario:
                existeCliente = True
                print("Ese usuario ya fue registrado")
                usuario = input("Ingrese otro usuario: ")
        
    nuevoCliente["Usuario"] = usuario

    #Contraseña
    while True:
            contraseña1 = input("Ingrese una contraseña (debe tener entre 8 y 12 caracteres, contener una mayúscula y un número): ")
 
            if not (8 <= len(contraseña1) <= 12):
                print("Error: La contraseña debe tener entre 8 y 12 caracteres.")
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
                elif not tiene_numero:
                    print("Error: La contraseña debe incluir al menos un número.")
                   
                else:
                    contraseña2 = input("Repita la contraseña: ")
                    if contraseña1 == contraseña2:
                        nuevoCliente["Contraseña"] = contraseña1
                        print("¡Usuario registrado exitosamente!")
                        return nuevoCliente
                    else:
                        print("Las contraseñas no coinciden. Intente de nuevo.")


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
        dni_actual = int(input("Ingrese su dni_actual sin puntos, ejemplo: XXXXXXXX: "))
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
                        limpiarPantalla()
                        print("Ingreso exitoso")
                        return cliente   # <-- DEVUELVE EL CLIENTE
        
        if not dni_actual_encontrado:
            limpiarPantalla()
            print("Algún dato se ingresó de manera incorrecta. ")
        
        continuar = int(input("¿Desea intentar ingresar nuevamente? 1=Reintentar, 2=Salir: "))
        if continuar == 2:
            return None
            print("Ha salido del sistema exitosamente.")


def sumarUsuarioALaBD(cliente, listaClientes):
    """
    Agrega un diccionario de cliente a una lista si no existe previamente.

    Comprueba si el diccionario 'cliente' ya se encuentra como un elemento dentro de 'listaClientes'. Si no se encuentra, lo agrega a la lista.

    Args:
        cliente (dict): Un diccionario que representa al cliente que se desea agregar.
        listaClientes (list): La lista de clientes donde se intentará agregar el nuevo cliente.

    Returns:
        list: La lista de clientes actualizada.
    """
    if cliente not in listaClientes:
        listaClientes.append(cliente)
    return listaClientes

def crearCuenta(listaClientes, dni_actual, tipoCuenta, moneda):

    """
    Intenta crear una nueva cuenta con saldo 0.0 para un cliente existente.

    La función busca un cliente por dni_actual en la lista.
    1. Si el cliente no se encuentra, imprime un error y retorna None.
    2. Si el cliente se encuentra, verifica si ya posee esa 'tipoCuenta'.
    3. Si ya la posee, imprime un aviso y no hace nada más.
    4. Si no la posee, agrega la clave 'tipoCuenta' al diccionario del cliente con un valor de 0.0, los datos de la cuenta (CBU y alias) en forma de tupla e imprime un mensaje de éxito.

    Esta función modifica el diccionario del cliente "in-place" (por referencia) dentro de la listaClientes original.

    Args:
        listaClientes (list): La lista de diccionarios de clientes.
        dni_actual (int): El dni_actual para buscar al cliente.
        tipoCuenta (str): El nombre de la clave para la nueva cuenta que se desea crear (ej: "CajaAhorroARS", "CuentaCorrienteUSD").
        moneda (str): El símbolo de la moneda (ej: "ARS", "USD") para usar en el mensaje de confirmación. No se almacena, solo se muestra en el 'print'.

    Returns:
        None: Esta función no retorna ningún valor útil. Su objetivo principal es modificar 'listaClientes' o imprimir mensajes en consola. Retorna 'None' explícitamente si el cliente no existe, e implícitamente 'None' en los demás casos.
    """
    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            clienteEncontrado = cliente
    
    if clienteEncontrado is None:
        limpiarPantalla()
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta in clienteEncontrado:
        limpiarPantalla()
        print(f"El cliente ya posee una cuenta en {tipoCuenta}")

    else:

        CBU =''.join([str(random.randint(0, 9)) for i in range(22)])
        
        ALIAS = clienteEncontrado["Usuario"] + '.bank'

        clienteEncontrado[tipoCuenta] = {
            "Saldo": 0.0,
            "Datos": (CBU,ALIAS) 
        }
        
        print(f"{tipoCuenta} creada exitosamente. Saldo inicial: 0.0 {moneda}. Datos: {clienteEncontrado[tipoCuenta]["Datos"]}")


def depositar(listaClientes, dni_actual, monto, tipoCuenta,  moneda):
    """
    Suma un monto específico al saldo de una cuenta de cliente existente.

    La función busca al cliente por dni_actual. Realiza las siguientes validaciones:
    1. Si el cliente no existe, imprime un error y retorna.
    2. Si la 'tipoCuenta' especificada no existe en el diccionario del cliente, imprime un error y retorna.
    3. Si el 'monto' a depositar es menor o igual a cero, imprime un error y retorna.

    Si todas las validaciones son exitosas, suma el 'monto' al saldo actual de la 'tipoCuenta' del cliente y muestra un mensaje de éxito.

    Esta función modifica el diccionario del cliente "in-place".

    Args:
        listaClientes (list): La lista de diccionarios de clientes.
        dni_actual (int): El dni_actual para buscar al cliente.
        monto (float): La cantidad de dinero a depositar. Debe ser un valor positivo.
        tipoCuenta (str): El nombre de la clave de la cuenta que recibirá el depósito (ej: "CajaAhorroARS").
        moneda (str): El símbolo de la moneda (ej: "ARS", "USD") para usar en el mensaje de confirmación.

    Returns:
        None: Esta función no retorna ningún valor. Su objetivo es modificar 'listaClientes' o imprimir mensajes en consola.
    """
    clienteEncontrado = None
    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            clienteEncontrado = cliente

    if clienteEncontrado is None:
        limpiarPantalla()
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta not in clienteEncontrado:
        limpiarPantalla()
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        return
    
    if monto <= 0:
        limpiarPantalla()
        print("El monto a depositar debe ser mayor a 0")
        return
    
    clienteEncontrado[tipoCuenta] +=monto
    limpiarPantalla()
    print(f"Depósito realizado con éxito. Saldo actual: {clienteEncontrado[tipoCuenta]: .2f} {moneda}")
    
    clienteEncontrado[tipoCuenta]["Saldo"] += monto
    print(f"Depósito realizado con éxito. Saldo actual: {clienteEncontrado[tipoCuenta]['Saldo']:.2f} {moneda}")


def consultarSaldo(listaClientes, dni_actual, tipoCuenta, moneda):
    """
    Muestra el saldo de una cuenta específica de un cliente si existe.

    Busca al cliente por su dni_actual en la lista. Realiza las siguientes validaciones:
    1. Si el cliente no se encuentra, imprime un error y retorna.
    2. Si el cliente se encuentra, pero no posee la 'tipoCuenta' especificada, imprime un error y retorna.

    Si tanto el cliente como la cuenta existen, imprime el saldo actual de esa cuenta, formateado a dos decimales.

    Args:
        listaClientes (list): La lista de diccionarios de clientes.
        dni_actual (int): El dni_actual para buscar al cliente.
        tipoCuenta (str): El nombre de la clave de la cuenta (ej: "CajaAhorroARS") cuyo saldo se desea consultar.
        moneda (str): El símbolo de la moneda (ej: "ARS", "USD") para usar en el mensaje que se muestra en consola.

    Returns:
        None: Esta función no retorna ningún valor. Su único objetivo es imprimir el saldo o un mensaje de error en la consola.
    """

    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["dni_actual"] == dni_actual:
            clienteEncontrado = cliente

    if clienteEncontrado is None:
        limpiarPantalla()
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta not in clienteEncontrado:
        limpiarPantalla()
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        return
     
    print(f"Saldo actual en {moneda}: {clienteEncontrado[tipoCuenta]['Saldo']:.2f} {moneda}")
    

def transferirEntreCuentas(listaClientes, dni_actual, origen, destino, monto, tasa=1000):
    """
    Transfiere un monto entre las cuentas en pesos y dólares de un cliente.

    La función busca al cliente por dni_actual. Asume que el cliente tiene un diccionario anidado llamado "Cuentas" (ej: {"Cuentas": {"Cuenta en pesos": 100}}).
    Si el diccionario "Cuentas" no existe, lo crea vacío.

    Realiza validaciones para asegurar que el cliente exista, la cuenta de origen exista y tenga saldo suficiente.

    El 'monto' se debita de la cuenta 'origen' en su moneda original y se acredita en la cuenta 'destino' aplicando la conversión de moneda correspondiente (usando las funciones lambda internas y la 'tasa').

    Args:
        listaClientes (list): La lista de diccionarios de clientes.
        dni_actual (int): El dni_actual para buscar al cliente.
        origen (str): El nombre exacto de la cuenta de origen (ej: "Cuenta en pesos" o "Cuenta en dólares").
        destino (str): El nombre exacto de la cuenta de destino (ej: "Cuenta en pesos" o "Cuenta en dólares").
        monto (float): El monto a transferir, expresado en la moneda de la cuenta 'origen'.
        tasa (float): La tasa de cambio (ARS por USD). Por defecto es 1000.

    Returns:
        None: Esta función no retorna ningún valor. Modifica el diccionario del cliente "in-place" e imprime mensajes en la consola.
    """

    # Lambdas para conversión
    usd_a_ars = lambda usd: usd * tasa
    ars_a_usd = lambda ars: ars / tasa

    # Buscar cliente
    cliente = None
    for c in listaClientes:
        limpiarPantalla()
        if c.get("dni_actual") == dni_actual:
            cliente = c

    # Verificaciones
    if cliente is None:
        limpiarPantalla()
        print("Cliente no encontrado.")
        return

    # Asegurarnos que la estructura de cuentas exista
    cliente.setdefault("Cuentas", {})

    cuentas = cliente["Cuentas"]

    if origen not in cuentas:
        limpiarPantalla()
        print("La cuenta de origen no existe.")
        return None

    saldo_origen = cuentas.get(origen, 0)
    if saldo_origen < monto:
        limpiarPantalla()
        print("Saldo insuficiente en la cuenta de origen.")
        return None

    # Actualizar saldos
    cuentas[origen] = saldo_origen - monto

    if origen == "Cuenta en pesos" and destino == "Cuenta en dólares":
        cuentas[destino] = cuentas.get(destino, 0) + ars_a_usd(monto)
        limpiarPantalla()
        print(f"Transferidos {monto:.2f} ARS a la cuenta en dólares.")

    elif origen == "Cuenta en dólares" and destino == "Cuenta en pesos":
        cuentas[destino] = cuentas.get(destino, 0) + usd_a_ars(monto)
        limpiarPantalla()
        print(f"Transferidos {monto:.2f} USD a la cuenta en pesos.")

    else:
        # Caso cuentas iguales o tipo inválido
        limpiarPantalla()
        print("Transferencia no válida (origen y destino iguales o nombres incorrectos).")

def limpiarPantalla():
    """
    En dicha funcion es para un fin estético para limpiar la terminal para que el 
    cliente opere más limpiamente.
    La primera condicion es para usuarios Windows y el segundo para MacOs y Linux
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



#MAIN

listaClientes = []
mostrar_menu = False #Es una bandera para mostrar el menú de movimientos dentro del HomeBanking, dependiendo de si se ingresó bien o no a la plataforma
cliente_actual = None

print("Bienvenido al HomeBanking, a continuación se visualizará un menú, elija la opción según corresponda: ")

opcionMain = int(input("1 para iniciar sesión, 2 para crear una cuenta: "))

if opcionMain == 1:
    cliente_actual = iniciarSesion(listaClientes)

    if cliente_actual is not None:
        print("Sesión iniciada correctamente")
        mostrar_menu = True

elif opcionMain == 2:
    nuevoCliente = registrarUsuario(listaClientes)
    if nuevoCliente is not None:
        sumarUsuarioALaBD(nuevoCliente, listaClientes)
        # Ingreso directo tras registrarse para simplificar (podés dejar tu pregunta si querés)
        cliente_actual = nuevoCliente
        print("Cuenta creada e iniciada sesión automáticamente.")
        mostrar_menu = True
    else:
        print("DNI ya registrado. Inicie sesión.")
else:
    print("Ingresó un valor incorrecto")


if mostrar_menu and cliente_actual:
    dni_actual = cliente_actual["dni_actual"]
    continuarOperaciones = True
    while continuarOperaciones:
        print("\n----MENÚ DE OPERACIONES----\n")
        print("1. Crear una cuenta en pesos")
        print("2. Depositar pesos")
        print("3. Consultar saldo en pesos")
        print("4. Crear una cuenta en dólares")
        print("5. Depositar dólares")
        print("6. Consultar saldo en dólares")
        print("7. Transferir entre cuentas")
        print("8. Salir")

        opcionCuentas = int(input("Ingrese un número del 1 al 8 según la operación que desee realizar: "))

        if opcionCuentas == 1:
            crearCuenta(listaClientes, dni_actual, "Cuenta en pesos", "ARS")

        elif opcionCuentas == 2:
            clienteEncontrado = None
            for c in listaClientes:
                if c.get("dni_actual") == dni_actual:
                    clienteEncontrado = c

            if "Cuenta en pesos" in clienteEncontrado:
                monto = float(input("Ingrese el monto a depositar en pesos: "))
                depositar(listaClientes, dni_actual, monto, "Cuenta en pesos", "ARS")
            else:
                print("No posee una cuenta en pesos. Debe crearla primero para depositar dinero.")

        elif opcionCuentas == 3:
            consultarSaldo(listaClientes, dni_actual, "Cuenta en pesos", "ARS")

        elif opcionCuentas == 4:
            crearCuenta(listaClientes, dni_actual, "Cuenta en dólares", "USD")

        elif opcionCuentas == 5:

            clienteEncontrado = None
            for c in listaClientes:
                if c.get("dni_actual") == dni_actual:
                    clienteEncontrado = c

            if "Cuenta en dólares" in clienteEncontrado:
                monto = float(input("Ingrese el monto a depositar en dólares: "))
                depositar(listaClientes, dni_actual, monto, "Cuenta en dólares", "USD")
            else:
                print("No posee una cuenta en dólares. Debe crearla primero para depositar dinero.")
   

        elif opcionCuentas == 6:
            consultarSaldo(listaClientes, dni_actual, "Cuenta en dólares", "USD")

        elif opcionCuentas == 7:
            monto = float(input("Ingrese el monto a transferir: "))

            print("Seleccione tipo de transferencia:")
            print("1. Pesos → Dólares")
            print("2. Dólares → Pesos")
            tipo = int(input("Opción: "))

            if tipo == 1:
                transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en pesos", "Cuenta en dólares", monto)
            elif tipo == 2:
                transferirEntreCuentas(listaClientes, dni_actual, "Cuenta en dólares", "Cuenta en pesos", monto)
            else:
                print("Opción inválida.")

        elif opcionCuentas == 8:
            print("Sesión finalizada. Muchas gracias.")
            continuarOperaciones = False

        else:
            print("Opción inválida")