import threading
import time
import random
def mostrar_menu():
    print("Seleccione las operaciones a realizar:")
    print("1. Generar facturas.")
    print("2. Generar registro de contabilidad.")
    print("3. Generar registro de inventario.")
    print("4. Salir")
class Producto:
    def __init__(self, nombre, precio, existencia_bodega1=0, existencia_bodega2=0):
        self.nombre = nombre
        self.precio = precio
        self.existencia_bodega1 = existencia_bodega1
        self.existencia_bodega2 = existencia_bodega2
        self.lock = threading.Lock()
    def agregar_existencia(self, bodega, cantidad):
        with self.lock:
            if bodega == 1:
                self.existencia_bodega1 += cantidad
            elif bodega == 2:
                self.existencia_bodega2 += cantidad

    def obtener_existencias(self):
        with self.lock:
            return {
                "Bodega 1": self.existencia_bodega1,
                "Bodega 2": self.existencia_bodega2
            }

class Factura:
    def __init__(self, cajero):
        self.cajero = cajero
        self.productos = []
        self.total = 0
        self.lock = threading.Lock()

    def agregar_producto(self, producto):
        with self.lock:
            self.productos.append(producto)
            self.total += producto.precio

    def generar_factura(self):
        with self.lock:
            contenido = f"Factura generada por el cajero {self.cajero}:\n" + \
                        "\n".join([f"{producto.nombre}: ${producto.precio}" for producto in self.productos]) + \
                        f"\nTotal: ${self.total}"

            with open(f"factura_{self.cajero}.txt", 'w') as archivo:
                archivo.write(contenido)

class Contabilidad:
    def __init__(self):
        self.total_ventas = 0
        self.lock = threading.Lock()

    def conciliar(self, monto):
        with self.lock:
            self.total_ventas += monto

    def obtener_total_ventas(self):
        with self.lock:
            return self.total_ventas

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def proceso_inventario(self, producto):
        existencias = analisis_imagen(producto)

        for bodega, cantidad in existencias.items():
            producto.agregar_existencia(int(bodega[-1]), cantidad)

        contenido = f"\nEstado del inventario para el producto {producto.nombre}:\n" + \
                    "\n".join([f"{bodega}: {cantidad}" for bodega, cantidad in producto.obtener_existencias().items()])

        with open("inventario_resultado.txt", 'w') as archivo:
            archivo.write(contenido)

def analisis_imagen(producto):
    # Simulamos un análisis de imagen para determinar existencias en las bodegas
    time.sleep(2)
    return {
        "Bodega 1": 50,  # Simulación de resultados ficticios
        "Bodega 2": 30
    }

def ejecutar_opcion(opcion, factura, contabilidad, inventario):
    if opcion == 1:
        factura.generar_factura()
        print("Facturas generadas.")
    elif opcion == 2:
        with open("contabilidad.txt", 'w') as archivo_contabilidad:
            archivo_contabilidad.write(f"Registro de contabilidad:\nTotal de ventas: ${contabilidad.obtener_total_ventas()}")
        print("Registro de contabilidad generado.")
    elif opcion == 3:
        with open("inventario.txt", 'w') as archivo_inventario:
            archivo_inventario.write("Registro de inventario:")
            for producto in inventario.productos:
                archivo_inventario.write(f"\nProducto: {producto.nombre}")
                archivo_inventario.write("\n".join([f"{bodega}: {cantidad}" for bodega, cantidad in producto.obtener_existencias().items()]))
        print("Registro de inventario generado.")
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    factura = Factura("CajeroPrincipal")
    contabilidad = Contabilidad()
    inventario = Inventario()

    while True:
        try:
            mostrar_menu()
            opcion = int(input("Ingrese el número de la opción deseada (4 para salir): "))
            if opcion == 4:
                break
            ejecutar_opcion(opcion, factura, contabilidad, inventario)
        except ValueError:
            print("Por favor, ingrese un número válido.")
