import datetime

listaRetiros = []

class Cuenta:
    def __init__(self, tipo_cuenta, id,ciudad, saldo_inicial=0):
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo_inicial
        self.ciudad= ciudad
        self.consignacion = []
        self.retiro = []
        self.movimientos = []
        self.id = id

    def consignar(self, monto, fecha=datetime.datetime.now()):

        if monto > 0:
            self.saldo += monto
            self.movimientos.append(f"Consignación: +${monto}, fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.consignar.append(f"Consignación: +${monto}, fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("El monto de la consignación debe ser mayor que cero.")

    def retirar(self, monto, ciudad, fecha=datetime.datetime.now()):
        if monto > 0 and self.saldo >= monto:
            self.ciudad= ciudad
            self.saldo -= monto
            info_transaccion =self.movimientos.append(f"Retiro: -${monto}, fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Ciudad {ciudad}")
            self.retiro.append(f"Retiro: -${monto}, fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Ciudad {ciudad}")
            if ciudad != Cuenta.ciudad and monto > 1000000:
                listaRetiros.append(self.id)
                
        else:
            print("Fondos insuficientes o monto inválido para el retiro.")

    def consultar_saldo(self):
        return self.saldo

    def consultar_movimientos(self):
        return self.movimientos

class Cliente:
    def __init__(self, nombre, ciudad, id):
        self.nombre = nombre
        self.ciudad = ciudad
        self.cuentas = []
        self.id = id

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def obtener_total_transacciones(self, mes):
        total = 0
        for cuenta in self.cuentas:
            for transaccion in cuenta.movimientos:
                if mes in transaccion:
                    total += 1
        return total

    def retiro_fuera_ciudad(self, monto_limite=1000000):
        for cuenta in self.cuentas:
            if any("retiro" in transaccion and cuenta.saldo - int(transaccion.split(":")[1]) >= monto_limite
                   for transaccion in cuenta.movimientos):
                return True
        return False

def menu_inicial():
    clientes = [Cliente("ivan", "Cali", "1144160384")]
    

    while True:
        print("Bienvenido al sistema bancario")
        print("Qué operación desea realizar?")
        print("1. Crear cuenta")
        print("2. Realizar depósito")
        print("3. Realizar retiro")
        print("4 consultar saldo")
        print("5 consultar movimientos")
        print("6 obtener total transacciones")
        print("7 lista de usuarios retirando fuera de la ciudad")
        print("8. Salir")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            crear_cuenta(clientes)
        elif opcion == "2":
            realizar_deposito(clientes)
        elif opcion == "3":
            realizar_retiro(clientes)
        elif opcion == "4":
            consultar_saldo(clientes)
        elif opcion == "5":
            consultar_movimientos(clientes)
        elif opcion == "6":
            obtener_total_transacciones(clientes)
        elif opcion == "7":
            lista_de_usuarios_retirando_fuera_de_la_ciudad(clientes)

        elif opcion == "8":
            print("Gracias por utilizar nuestro sistema bancario. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número válido.")

def crear_cuenta(clientes):
    id = input("Ingrese el id del cliente: ")
    if any(cliente.id == id for cliente in clientes):
        print("El id ingresado ya se encuentra registrado.")
        agregar_cuenta = input("Desea agregar una cuenta? (s/n): ")
        if agregar_cuenta.lower() == "n":
            print("No se creó la cuenta.")
        else:
            cliente = next(cliente for cliente in clientes if cliente.id == id)
            tipo_cuenta = input("Ingrese el tipo de cuenta: ")
            if any(cuenta.tipo_cuenta == tipo_cuenta for cuenta in cliente.cuentas):
                print("Ya tiene una cuenta de este tipo.")
                return
            saldo_inicial = float(input("Ingrese el saldo inicial: "))
            cuenta = Cuenta(tipo_cuenta, id, saldo_inicial)
            cliente.agregar_cuenta(cuenta)

            print("Cuenta creada exitosamente.")
        return
    else:
        nombre = input("Ingrese el nombre del cliente: ")
        ciudad = input("Ingrese la ciudad del cliente: ")
        cliente = Cliente(nombre, ciudad, id)
        clientes.append(cliente)
        tipo_cuenta = input("Ingrese el tipo de cuenta: ")
        saldo_inicial = float(input("Ingrese el saldo inicial: "))

        cuenta = Cuenta(tipo_cuenta, id, saldo_inicial)
        cliente.agregar_cuenta(cuenta)

        print("Cuenta creada exitosamente.")

def realizar_deposito(clientes):
    id = input("Ingrese el id del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.id == id), None)
    if cliente:
        cuenta = seleccionar_cuenta(cliente)
        if cuenta:
            monto = float(input("Ingrese el monto a depositar: "))
            cuenta.consignar(monto)
            print("Depósito realizado exitosamente.")
        else:
            print("No se pudo seleccionar la cuenta.")
    else:
        print("Cliente no encontrado.")

def realizar_retiro(clientes):
    id = input("Ingrese el id del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.id == id), None)
    if cliente:
        cuenta = seleccionar_cuenta(cliente)
        if cuenta:
            monto = float(input("Ingrese el monto a retirar: "))
            ciudad = input("Ingrese la ciudad del retiro: ")
            cuenta.retirar(monto, ciudad)
            print("Retiro realizado exitosamente.")
        else:
            print("No se pudo seleccionar la cuenta.")
    else:
        print("Cliente no encontrado.")

def seleccionar_cuenta(cliente):
    if len(cliente.cuentas) == 0:
        print("No tiene cuentas asociadas.")
        return None

    print("Cuentas disponibles:")
    for i, cuenta in enumerate(cliente.cuentas):
        print(f"{i+1}. {cuenta.tipo_cuenta}")

    opcion = input("Ingrese el número de la cuenta deseada: ")
    if opcion.isdigit() and int(opcion) in range(1, len(cliente.cuentas)+1):
        return cliente.cuentas[int(opcion)-1]
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")
        return None
    
def consultar_saldo(clientes):
    id = input("Ingrese el id del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.id == id), None)
    if cliente:
        cuenta = seleccionar_cuenta(cliente)
        if cuenta:
            saldo = cuenta.consultar_saldo()
            print(f"El saldo de la cuenta es: ${saldo}")
        else:
            print("No se pudo seleccionar la cuenta.")
    else:
        print("Cliente no encontrado.")

def consultar_movimientos(clientes):
    id = input("Ingrese el id del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.id == id), None)
    if cliente:
        cuenta = seleccionar_cuenta(cliente)
        if cuenta:
            movimientos = cuenta.consultar_movimientos()
            print("Movimientos:")
            for movimiento in movimientos:
                print(movimiento)
        else:
            print("No se pudo seleccionar la cuenta.")
    else:
        print("Cliente no encontrado.")

def obtener_total_transacciones(clientes):
    id = input("Ingrese el id del cliente: ")
    cliente = next((cliente for cliente in clientes if cliente.id == id), None)
    if cliente:
        mes = input("Ingrese el mes a consultar (formato: YYYY-MM): ")
        if mes == "":
            print("Mes inválido.")
            return
        if any(cliente.obtener_total_transacciones(mes) > 0 for cliente in clientes):
            total = cliente.obtener_total_transacciones(mes)
            print(f"El total de transacciones en el mes {mes} es: {total}")
        if cliente:
            cuenta = seleccionar_cuenta(cliente)
            if cuenta:
                movimientos = cuenta.consultar_movimientos()
                print("Movimientos:")
                for movimiento in movimientos:
                    print(movimiento)
                print(f"Saldo: {cuenta.consultar_saldo()}")

    else:
        print("Cliente no encontrado.")


def lista_de_usuarios_retirando_fuera_de_la_ciudad(clientes):
    for cliente in clientes:
        if cliente.retiro.ciudad != Cuenta.ciudad():
            listaRetiros.append(cliente.nombre)
    if listaRetiros:
        print("Los siguientes clientes han retirado más de $1'000.000 fuera de su ciudad:")
        print(listaRetiros.sort())
            
            
menu_inicial()
