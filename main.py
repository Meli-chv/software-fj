# main.py
# Programa principal: simula operaciones validas e invalidas para demostrar
# que el sistema sigue funcionando aunque ocurran errores.

from sistema import SistemaFJ
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from excepciones import SoftwareFJError
from registro import registrar_evento, registrar_error, ARCHIVO_LOG


def titulo(numero, texto):
    # Funcion auxiliar para imprimir el encabezado de cada operacion
    print(f"\nOperacion {numero}: {texto}")


def main():
    registrar_evento("===== Inicio de la simulacion Software FJ =====")
    sistema = SistemaFJ()

    # ---------------- CLIENTES ----------------
    titulo(1, "Registrar cliente valido")
    ana = sistema.registrar_cliente("Ana Torres", "1023456789", "ana.torres@correo.com", "3104567890")

    titulo(2, "Registrar otro cliente valido")
    luis = sistema.registrar_cliente("Luis Gomez", "80123456", "luis.gomez@correo.com", "3209876543")

    titulo(3, "Cliente con correo invalido")
    sistema.registrar_cliente("Pedro Ruiz", "52987654", "pedro.correo.com", "3001112233")

    titulo(4, "Cliente con nombre que tiene numeros")
    sistema.registrar_cliente("M4ria", "12AB", "maria@correo.com", "3001112233")

    titulo("4b", "Cliente con documento que tiene letras")
    sistema.registrar_cliente("Maria Lopez", "12AB", "maria@correo.com", "3001112233")

    titulo(5, "Cliente con parametro faltante (telefono vacio)")
    sistema.registrar_cliente("Carla Diaz", "1098765432", "carla@correo.com", "")

    titulo(6, "Cliente con documento repetido")
    sistema.registrar_cliente("Ana Maria Torres", "1023456789", "otra@correo.com", "3104567891")

    # ---------------- SERVICIOS ----------------
    titulo(7, "Crear tres servicios validos (uno de cada tipo)")
    sala = sistema.agregar_servicio(ReservaSala, "Sala Andes", 50000, capacidad=30)
    portatiles = sistema.agregar_servicio(AlquilerEquipo, "Portatiles", 15000, cantidad=3, deposito=100000)
    asesoria = sistema.agregar_servicio(Asesoria, "Asesoria en Redes", 120000, nivel="experto")

    titulo(8, "Crear servicios invalidos")
    sistema.agregar_servicio(ReservaSala, "Sala Mini", -20000, capacidad=4)        # tarifa negativa
    sistema.agregar_servicio(Asesoria, "Asesoria Cloud", 90000, nivel="maestro")    # nivel no existe
    sistema.agregar_servicio(AlquilerEquipo, "Videobeam", 30000)                    # faltan parametros

    # ---------------- RESERVAS ----------------
    titulo(9, "Reserva exitosa de sala con 10% de descuento")
    r1 = sistema.crear_reserva(ana, sala, 4, descuento=0.10)

    titulo(10, "Reserva exitosa de asesoria")
    r2 = sistema.crear_reserva(luis, asesoria, 2.5)

    titulo(11, "Reserva con duracion no permitida (excepcion encadenada)")
    sistema.crear_reserva(luis, portatiles, 1)   # minimo son 2 horas

    titulo(12, "Reserva con cliente inexistente (None)")
    sistema.crear_reserva(None, sala, 2)

    titulo(13, "Reserva con descuento fuera de rango")
    sistema.crear_reserva(ana, portatiles, 5, descuento=0.9)

    titulo(14, "Procesar reserva y luego intentar reservar el servicio ocupado")
    try:
        r1.procesar()
        print(f"   [OK] Reserva procesada: {r1}")
    except SoftwareFJError as e:
        print(f"   [X] Error: {e}")
    sistema.crear_reserva(luis, sala, 2)   # la sala ya no esta disponible

    titulo(15, "Operaciones no permitidas sobre reservas")
    # Cancelar una reserva que ya fue procesada
    try:
        r1.cancelar("El cliente se arrepintio")
    except SoftwareFJError as e:
        registrar_error(e, "cancelar")
        print(f"   [X] Error: {e}")
    # Cancelar correctamente la reserva de asesoria
    try:
        r2.cancelar("Cambio de fecha")
        print(f"   [OK] Reserva cancelada: {r2}")
    except SoftwareFJError as e:
        print(f"   [X] Error: {e}")
    # Intentar procesar una reserva cancelada
    try:
        r2.procesar()
    except SoftwareFJError as e:
        print(f"   [X] Error: {e}")

    titulo(16, "Metodo sobrecargado: distintas formas de calcular el costo")
    print(f"   Base (3 h):              ${asesoria.calcular_costo(3):,.2f}")
    print(f"   Con IVA:                 ${asesoria.calcular_costo(3, impuesto=True):,.2f}")
    print(f"   Con 20% de descuento:    ${asesoria.calcular_costo(3, descuento=0.2):,.2f}")
    print(f"   Con IVA y descuento:     ${asesoria.calcular_costo(3, impuesto=True, descuento=0.2):,.2f}")

    # ---------------- RESUMEN ----------------
    sistema.resumen()
    registrar_evento("===== Fin de la simulacion =====")
    print(f"\nEl programa termino sin interrupciones. Revisa el archivo '{ARCHIVO_LOG}'.")


if __name__ == "__main__":
    # Ultima red de seguridad: si algo inesperado pasa, se registra y no se cae feo
    try:
        main()
    except Exception as e:
        registrar_error(e, "error inesperado en main")
        print(f"Ocurrio un error inesperado: {e}")
