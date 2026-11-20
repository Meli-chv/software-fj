# sistema.py
# Clase que administra las listas internas de clientes, servicios y reservas.
# No se usa base de datos: todo queda en listas de Python mientras corre el programa.

from cliente import Cliente
from reserva import Reserva
from excepciones import SoftwareFJError, OperacionNoPermitidaError
from registro import registrar_evento, registrar_error


class SistemaFJ:

    def __init__(self):
        # Listas internas (aqui vive toda la informacion)
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, documento, correo, telefono):
        """Crea y guarda un cliente. Devuelve el cliente o None si fallo."""
        try:
            # No se permiten dos clientes con el mismo documento
            if any(c.documento == str(documento) for c in self.clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente con documento {documento}")
            cliente = Cliente(nombre, documento, correo, telefono)
        except SoftwareFJError as e:
            registrar_error(e, "registrar_cliente")
            print(f"   [X] Error: {e}")
            return None
        else:
            self.clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente.describir()}")
            print(f"   [OK] Cliente registrado: {cliente}")
            return cliente

    def agregar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea un servicio de cualquier tipo (polimorfismo) y lo agrega a la lista."""
        try:
            servicio = clase_servicio(*args, **kwargs)
        except SoftwareFJError as e:
            registrar_error(e, f"agregar_servicio({clase_servicio.__name__})")
            print(f"   [X] Error: {e}")
            return None
        except TypeError as e:
            # Pasa si faltan argumentos al crear la clase
            registrar_error(e, f"agregar_servicio({clase_servicio.__name__})")
            print(f"   [X] Error de parametros: {e}")
            return None
        else:
            self.servicios.append(servicio)
            registrar_evento(f"Servicio creado: {servicio.describir()}")
            print(f"   [OK] Servicio creado: {servicio}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas, descuento=0.0):
        """Crea y confirma una reserva."""
        try:
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar(descuento)
        except SoftwareFJError as e:
            registrar_error(e, "crear_reserva")
            print(f"   [X] Error: {e}")
            # Si hay una causa encadenada la muestro tambien
            if e.__cause__:
                print(f"       Causa: {e.__cause__}")
            return None
        else:
            self.reservas.append(reserva)
            print(f"   [OK] Reserva confirmada: {reserva}")
            return reserva
        finally:
            registrar_evento("Fin del intento de crear reserva")

    def resumen(self):
        print(f"\nClientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | "
              f"Reservas: {len(self.reservas)}")
        for r in self.reservas:
            print(f"   {r}")
