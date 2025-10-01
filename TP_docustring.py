"""
HomeBanking básico con registro, login, cuentas y operaciones simples.
"""

def registrarUsuario(listaClientes):
    """Registra un cliente validando DNI, usuario único y contraseña válida."""
    nuevoCliente = {}

    #DNI
    DNI = int(input("Ingrese su DNI, sin puntos: XXXXXXXX "))

    for cliente in listaClientes:
        if cliente["DNI"] == DNI:
            print("El usuario ya esta registrado, inicie sesión. ")
            return  

    nuevoCliente["DNI"] = DNI

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
        contraseña1 = input("Ingrese una contraseña, debe ser minimo de 8 caracteres y máximo de 12: ")

        if 8 <= len(contraseña1) <= 12:
            contraseña2 = input("Repita la contraseña: ")
            if contraseña1 == contraseña2:
                nuevoCliente["Contraseña"] = contraseña1
                return nuevoCliente
            else:
                print("La contraseñas no coinciden. ")
        else:
            print("La contraseña no cumple con los requisitos. ")


def iniciarSesion(lista):
    """Verifica DNI, usuario y contraseña para iniciar sesión con reintentos."""
    while True:
        DNI = int(input("Ingrese su DNI sin puntos, ejemplo: XXXXXXXX: "))
        dni_encontrado = False
        
        for cliente in lista:
            if cliente["DNI"] == DNI:
                dni_encontrado = True
                usuario = input("Ingrese su usuario: ")
                
                if cliente["Usuario"] == usuario:
                    contraseña = input("Ingrese su contraseña: ")
                    
                    if cliente["Contraseña"] == contraseña:
                        print("Ingreso exitoso")
                        return True
        
        if not dni_encontrado:
            print("Algún dato se ingresó de manera incorrecta. ")
        
        continuar = int(input("¿Desea intentar ingresar nuevamente? Para volver a ingresar ingrese 1, para salir ingrese 2: "))
        if continuar == 2:
            return False


def sumarUsuarioALaBD(cliente, listaClientes):
    """Agrega un cliente nuevo a la lista si aún no existe."""
    if cliente not in listaClientes:
        listaClientes.append(cliente)
    return listaClientes


def crearCuenta(listaClientes, DNI, tipoCuenta, moneda):
    """Crea una cuenta en ARS o USD si el cliente existe y no la tiene."""
    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["DNI"] == DNI:
            clienteEncontrado = cliente
    
    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta in clienteEncontrado:
        print(f"El cliente ya posee una cuenta en {tipoCuenta}")
    else:
        clienteEncontrado[tipoCuenta] = 0.0
        print(f"{tipoCuenta} creada exitosamente. Saldo inicial: 0.0 {moneda}")


def depositar(listaClientes, DNI, monto, tipoCuenta,  moneda):
    """Deposita un monto en la cuenta indicada si el cliente existe."""
    clienteEncontrado = None
    for cliente in listaClientes:
        if cliente["DNI"] == DNI:
            clienteEncontrado = cliente

    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta not in clienteEncontrado:
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        return
    
    if monto <= 0:
        print("El monto a depositar debe ser mayor a 0")
        return
    
    clienteEncontrado[tipoCuenta] +=monto
    print(f"Depósito realizado con éxito. Saldo actual: {clienteEncontrado[tipoCuenta]: .2f} {moneda}")
    

def consultarSaldo(listaClientes, DNI, tipoCuenta, moneda):
    """Muestra el saldo de la cuenta indicada si existe."""
    clienteEncontrado = None

    for cliente in listaClientes:
        if cliente["DNI"] == DNI:
            clienteEncontrado = cliente

    if clienteEncontrado is None:
        print("El cliente no se encuentra dentro del sistema")
        return None
    
    if tipoCuenta not in clienteEncontrado:
        print(f"El cliente no posee una cuenta en {tipoCuenta}. Debe crearla primero")
        return
     
    print(f"Saldo actual en {moneda}: {clienteEncontrado[tipoCuenta]:.2f} {moneda}")

def transferirEntreCuentas(listaClientes, DNI, origen, destino, monto, tasa=1000):
    """
    Transfiere dinero entre cuentas de un cliente (Pesos <-> Dólares) sin usar 'break'.
    Usa lambdas para convertir monedas (ARS <-> USD).

    Parámetros:
        listaClientes (list): lista con los clientes registrados
        DNI (int): documento del cliente
        origen (str): "Cuenta en pesos" o "Cuenta en dólares"
        destino (str): "Cuenta en pesos" o "Cuenta en dólares"
        monto (float): monto a transferir
        tasa (float): cotización del dólar (1 USD = tasa ARS)
    """
    # Lambdas para conversión
    usd_a_ars = lambda usd: usd * tasa
    ars_a_usd = lambda ars: ars / tasa

    # Buscar cliente
    cliente = None
    for c in listaClientes:
        if c.get("DNI") == DNI:
            cliente = c

    # Verificaciones
    if cliente is None:
        print("Cliente no encontrado.")
        return

    # Asegurarnos que la estructura de cuentas exista
    cliente.setdefault("Cuentas", {})

    cuentas = cliente["Cuentas"]

    if origen not in cuentas:
        print("La cuenta de origen no existe.")
        return

    saldo_origen = cuentas.get(origen, 0)
    if saldo_origen < monto:
        print("Saldo insuficiente en la cuenta de origen.")
        return

    # Actualizar saldos
    cuentas[origen] = saldo_origen - monto

    if origen == "Cuenta en pesos" and destino == "Cuenta en dólares":
        cuentas[destino] = cuentas.get(destino, 0) + ars_a_usd(monto)
        print(f"Transferidos {monto:.2f} ARS a la cuenta en dólares.")

    elif origen == "Cuenta en dólares" and destino == "Cuenta en pesos":
        cuentas[destino] = cuentas.get(destino, 0) + usd_a_ars(monto)
        print(f"Transferidos {monto:.2f} USD a la cuenta en pesos.")

    else:
        # Caso cuentas iguales o tipo inválido
        print("Transferencia no válida (origen y destino iguales o nombres incorrectos).")


#MAIN

listaClientes = []
mostrar_menu = False #Es una bandera para mostrar el menú de movimientos dentro del HomeBanking, dependiendo de si se ingresó bien o no a la plataforma

print("Bienvenido al HomeBanking, a continuación se visualizará un menú, elija la opción según corresponda: ")

opcionMain = int(input("1 para iniciar sesión, 2 para crear una cuenta: "))

if opcionMain == 1:
    ingresoUsuario = iniciarSesion(listaClientes)

    if ingresoUsuario == True:
        print("Sesión iniciada correctamente")
        mostrar_menu = True

elif opcionMain == 2:
    nuevoCliente = registrarUsuario(listaClientes)

    actualizarBD = sumarUsuarioALaBD(nuevoCliente, listaClientes)

    opcionInicioSesion = int(input("Ahora que creó una cuenta, desea iniciar sesión? Ingrese 1 para iniciar sesión, 2 para no iniciar sesión: "))

    ingresoUsuario = iniciarSesion(listaClientes)
    if opcionInicioSesion == 1 and ingresoUsuario == True:
        mostrar_menu = True
        

    elif opcionInicioSesion == 2:
        print("Ha salido de la página de HomeBanking.")
        mostrar_menu = False
    
    else:
        print("Ingresó un valor incorrecto")

else:
    print("Ingresó un valor incorrecto")


if mostrar_menu == True:
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
            DNI = int(input("Ingrese su DNI: "))
            crearCuenta(listaClientes, DNI, "Cuenta en pesos", "ARS")

        elif opcionCuentas == 2:
            DNI = int(input("Ingrese su DNI: "))
            monto = float(input("Ingrese el monto a depositar en pesos: "))
            depositar(listaClientes, DNI, monto, "Cuenta en pesos", "ARS")

        elif opcionCuentas == 3:
            DNI = int(input("Ingrese su DNI: "))
            consultarSaldo(listaClientes, DNI, "Cuenta en pesos", "ARS")

        elif opcionCuentas == 4:
            DNI = int(input("DNI: "))
            crearCuenta(listaClientes, DNI, "Cuenta en dólares", "USD")

        elif opcionCuentas == 5:
            DNI = int(input("DNI: "))
            monto = float(input("Ingrese el monto a depositar en dólares: "))
            depositar(listaClientes, DNI, monto, "Cuenta en dólares", "USD")

        elif opcionCuentas == 6:
            DNI = int(input("DNI: "))
            consultarSaldo(listaClientes, DNI, "Cuenta en dólares", "USD")

        elif opcionCuentas == 7:
            DNI = int(input("Ingrese su DNI: "))
            monto = float(input("Ingrese el monto a transferir: "))

            print("Seleccione tipo de transferencia:")
            print("1. Pesos → Dólares")
            print("2. Dólares → Pesos")
            tipo = int(input("Opción: "))

            if tipo == 1:
                transferirEntreCuentas(listaClientes, DNI, "Cuenta en pesos", "Cuenta en dólares", monto)
            elif tipo == 2:
                transferirEntreCuentas(listaClientes, DNI, "Cuenta en dólares", "Cuenta en pesos", monto)
            else:
                print("Opción inválida.")

        elif opcionCuentas == 8:
            print("Sesión finalizada. Muchas gracias.")
            continuarOperaciones = False

        else:
            print("Opción inválida")


