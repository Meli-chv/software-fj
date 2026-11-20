# excepciones.py
# Aqui defino las excepciones personalizadas del sistema Software FJ.
# Todas heredan de una excepcion base para poder capturarlas juntas si se necesita.


class SoftwareFJError(Exception):
    """Excepcion base de todo el sistema."""

    def __init__(self, mensaje, codigo="ERR-000"):
        # Llamo al constructor de Exception con el mensaje
        super().__init__(mensaje)
        # Guardo un codigo para identificar el tipo de error en el log
        self.codigo = codigo

    def __str__(self):
        # Muestro el codigo junto al mensaje para que sea facil de leer
        return f"[{self.codigo}] {self.args[0]}"


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las validaciones (correo, documento, etc.)."""

    def __init__(self, campo, valor, motivo):
        # Armo un mensaje que diga que campo fallo y por que
        mensaje = f"Dato invalido en '{campo}' ({valor!r}): {motivo}"
        super().__init__(mensaje, "ERR-DAT")
        self.campo = campo


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parametro obligatorio."""

    def __init__(self, parametro):
        super().__init__(f"Falta el parametro obligatorio '{parametro}'", "ERR-PAR")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no esta disponible."""

    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no esta disponible", "ERR-SRV")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no se puede crear o procesar."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-RES")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una accion que no esta permitida en ese estado."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-OPE")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un calculo de costos da un resultado que no tiene sentido."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-CAL")
