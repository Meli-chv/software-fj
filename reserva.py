# reserva.py
# Clase Reserva: une un cliente con un servicio, una duracion y un estado.

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, DatosInvalidosError)
from registro import registrar_evento, registrar_error


class Reserva(Entidad):
    """Una reserva pasa por los estados: PENDIENTE -> CONFIRMADA -> PROCESADA, o CANCELADA."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, horas):
        # Verifico que me pasen objetos del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente valido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio valido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre)

        # Encadenamiento: si la duracion no es valida para el servicio,
        # convierto el error de datos en un error de reserva, guardando la causa
        try:
            servicio.validar_parametros(horas)
        except DatosInvalidosError as e:
            raise ReservaInvalidaError(f"Duracion no valida para {servicio.nombre}") from e

        super().__init__("RES")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE
        self._total = 0.0

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self, descuento=0.0):
        """Confirma la reserva y calcula el total con IVA."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar {self.id}: esta en estado {self._estado}")
        # try/except/else: si el calculo sale bien, en el else cambio el estado
        try:
            total = self._servicio.calcular_costo(self._horas, impuesto=True, descuento=descuento)
        except DatosInvalidosError as e:
            raise ReservaInvalidaError(f"No se pudo calcular el costo de {self.id}") from e
        else:
            self._total = total
            self._estado = self.CONFIRMADA
            registrar_evento(f"Reserva {self.id} confirmada. Total: ${total:,.2f}")

    def cancelar(self, motivo="Sin motivo"):
        """Cancela la reserva si todavia no se ha procesado."""
        if self._estado in (self.PROCESADA, self.CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar {self.id}: ya esta {self._estado}")
        self._estado = self.CANCELADA
        registrar_evento(f"Reserva {self.id} cancelada. Motivo: {motivo}")

    def procesar(self):
        """Procesa (cobra) la reserva. Usa try/except/finally."""
        try:
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas confirmadas ({self.id} esta {self._estado})")
            # Al procesar, el servicio queda ocupado
            self._servicio.cambiar_disponibilidad(False)
            self._estado = self.PROCESADA
            registrar_evento(f"Reserva {self.id} procesada para {self._cliente.nombre}")
        except OperacionNoPermitidaError as e:
            registrar_error(e, "procesar")
            raise  # vuelvo a lanzar para que quien llamo sepa que fallo
        finally:
            # Esto se ejecuta siempre, haya error o no
            registrar_evento(f"Intento de procesamiento de {self.id} finalizado (estado: {self._estado})")

    def validar(self):
        return self._horas > 0 and self._cliente.validar() and self._servicio.validar()

    def describir(self):
        return (f"{self.id} | {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | ${self._total:,.2f}")
