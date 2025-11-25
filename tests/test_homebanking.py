from homebanking import transferir_entre_cuentas
from homebanking import depositar
from homebanking import crear_cuenta


def test_transferir_entre_cuentas():
    lista_prueba = [
        {
            "dni_actual": 46212624,
            "Cuenta en pesos": {"Saldo": 10000},
            "Cuenta en dólares": {"Saldo": 0}
        }
    ]
    
    transferir_entre_cuentas(lista_prueba, 46212624, "Cuenta en pesos", "Cuenta en dólares", 1000, tasa=1000)

    assert lista_prueba[0]["Cuenta en pesos"]["Saldo"] == 9000
    assert lista_prueba[0]["Cuenta en dólares"]["Saldo"] == 1 


def test_depositar_pesos():
    lista_prueba = [
        {
            "dni_actual": 46212624,
            "Cuenta en pesos": {"Saldo": 5000}
        }
    ]

    depositar(lista_prueba, 46212624, 1000, "Cuenta en pesos", "ARS")

    assert lista_prueba[0]["Cuenta en pesos"]["Saldo"] == 6000


def test_crear_cuenta_pesos():
    lista = [
        {"dni_actual": 46212624, "Usuario": "taccorinti"}
    ]

    crear_cuenta(lista, 46212624, "Cuenta en pesos", "ARS")

    assert "Cuenta en pesos" in lista[0]
    assert lista[0]["Cuenta en pesos"]["Saldo"] == 0