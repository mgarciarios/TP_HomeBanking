#Con esta función buscamos registrar al usuario y validar que no este ya en la lista de usuarios registrados en el HomeBanking
def registrarUsuario(listaClientes):

    nuevoCliente = {}

    #DNI
    DNI = int(input("Ingrese su DNI, sin puntos: XXXXXXXX "))

    for cliente in listaClientes:
        if cliente["DNI"] == DNI:
            print("El usuario ya esta registrado, inicie sesión. ")
            return  
            #En caso de que ya exista un usuario con ese DNI, sale de la función porque es un identificador único.

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
                return nuevoCliente
            else:
                print("La contraseñas no coinciden. ")
        else:
            print("La contraseña no cumple con los requisitos. ")

    nuevoCliente["Contraseña"] = contraseña1


#Con esta función validamos que ingrsa todos los datos correctamente hasta iniciar sesión. 
def iniciarSesion(lista):
    ingreso = False

    while ingreso == False:

        DNI = int(input("Ingrese su DNI sin puntos, ejemplo: XXXXXXXX: "))

        for cliente in lista:

            if cliente["DNI"] == DNI:
                usuario = input("Ingrese su usuario: ")
                
                if cliente["Usuario"] == usuario:
                    contraseña = input("Ingrese su contraseña: ")

                    if cliente["Contraseña"] == contraseña:
                        print("Ingreso existoso: ")
                        ingreso = True
                        break

        if ingreso == False:
            print("Datos incorrectos. Intente nuevamente: ") 


def sumarUsuarioALaBD(cliente, listaClientes):
    if cliente not in listaClientes:
        listaClientes.append(cliente)
    return listaClientes

"""
def crearCuentaPesos():
def crearCuentaDolares():
def consultarCuentaPesos():
def consultarCuentaDolares():
"""



#MAIN

listaClientes = []

print("Bienvenido al HomeBanking, a continuación se visualizará un menú, elija la opción según corresponda: ")

opcionMain = int(input("1 para iniciar sesión, 2 para crear una cuenta: "))

if opcionMain == 1:
    ingresoUsuario = iniciarSesion(listaClientes)

elif opcionMain == 2:
    nuevoCliente = registrarUsuario(listaClientes)
    actualizarBD = sumarUsuarioALaBD(nuevoCliente, listaClientes)

    opcionInicioSesion = int(input("Ahora que creó una cuenta, desea iniciar sesión? Ingrese 1 para iniciar sesión, 2 para no iniciar sesión: "))

    if opcionInicioSesion == 1:
        ingresoUsuario = iniciarSesion(listaClientes)

    elif opcionInicioSesion == 2:
        print("Ha salido de la página de HomeBanking.")
    
    else:
        print("Ingresó un valor incorrecto")


else:
    print("Ingresó un valor incorrecto")