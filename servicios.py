# servicios.py
# Clase abstracta Servicio y los tres servicios que ofrece Software FJ:
# reserva de salas, alquiler de equipos y asesorias especializadas.

from abc import abstractmethod
from entidad import Entidad
from excepciones import (DatosInvalidosError, ParametroFaltanteError,
                         CalculoInconsistenteError)


class Servicio(Entidad):
    """Clase abstracta para todos los servicios."""

    IVA = 0.19  # impuesto por defecto en Colombia

    def __init__(self, nombre, tarifa_hora, disponible=True):
        if not nombre:
            raise ParametroFaltanteError("nombre del servicio")
        # La tarifa tiene que ser un numero mayor que cero
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatosInvalidosError("tarifa_hora", tarifa_hora, "debe ser un numero mayor que 0")
        super().__init__("SRV")
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = bool(estado)

    # ---------- Metodo "sobrecargado" ----------
    # Python no permite varios metodos con el mismo nombre, entonces la
    # sobrecarga se hace con parametros opcionales. Se puede llamar de 4 formas:
    #   calcular_costo(horas)                          -> costo base
    #   calcular_costo(horas, impuesto=True)           -> con IVA
    #   calcular_costo(horas, descuento=0.1)           -> con descuento
    #   calcular_costo(horas, impuesto=True, descuento=0.1) -> ambos
    def calcular_costo(self, horas, impuesto=False, descuento=0.0):
        # Valido que las horas tengan sentido
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("horas", horas, "deben ser mayores que 0")
        # El descuento va entre 0 y 50%
        if not 0 <= descuento <= 0.5:
            raise DatosInvalidosError("descuento", descuento, "debe estar entre 0 y 0.5")

        # Cada servicio calcula su base distinto (polimorfismo)
        costo = self._costo_base(horas)
        costo = costo * (1 - descuento)
        if impuesto:
            costo = costo * (1 + self.IVA)

        # Si por algun motivo el costo da negativo o cero, algo esta mal
        if costo <= 0:
            raise CalculoInconsistenteError(f"Costo calculado no valido: {costo}")
        return round(costo, 2)

    @abstractmethod
    def _costo_base(self, horas):
        """Cada servicio define como calcula su costo antes de impuestos."""
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        """Cada servicio tiene sus propias reglas de duracion."""
        pass

    def validar(self):
        return self._tarifa_hora > 0


class ReservaSala(Servicio):
    """Alquiler de salas de reuniones."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("capacidad", capacidad, "debe ser un entero positivo")
        self._capacidad = capacidad

    def _costo_base(self, horas):
        # Las salas grandes (mas de 20 personas) tienen un recargo del 20%
        recargo = 1.2 if self._capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def validar_parametros(self, horas):
        # Una sala se puede reservar maximo 12 horas seguidas
        if horas > 12:
            raise DatosInvalidosError("horas", horas, "una sala se reserva maximo 12 horas")
        return True

    def describir(self):
        return f"{self.id} | Sala '{self.nombre}' | {self._capacidad} personas | ${self.tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portatiles, videobeam, etc.)."""

    def __init__(self, nombre, tarifa_hora, cantidad, deposito, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("cantidad", cantidad, "debe ser un entero positivo")
        if deposito < 0:
            raise DatosInvalidosError("deposito", deposito, "no puede ser negativo")
        self._cantidad = cantidad
        self._deposito = deposito

    def _costo_base(self, horas):
        # Se cobra por equipo y por hora, mas un deposito fijo
        return self._tarifa_hora * horas * self._cantidad + self._deposito

    def validar_parametros(self, horas):
        # Los equipos se alquilan minimo 2 horas y maximo 72 (3 dias)
        if not 2 <= horas <= 72:
            raise DatosInvalidosError("horas", horas, "el alquiler va de 2 a 72 horas")
        return True

    def describir(self):
        return (f"{self.id} | Equipo '{self.nombre}' x{self._cantidad} | "
                f"${self.tarifa_hora:,.0f}/h | deposito ${self._deposito:,.0f}")


class Asesoria(Servicio):
    """Asesorias especializadas con un consultor."""

    NIVELES = {"basico": 1.0, "intermedio": 1.3, "experto": 1.7}

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise DatosInvalidosError("nivel", nivel, f"debe ser uno de {list(self.NIVELES)}")
        self._nivel = nivel

    def _costo_base(self, horas):
        # El precio sube segun el nivel del asesor
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def validar_parametros(self, horas):
        # Las asesorias se cobran por bloques de media hora, maximo 8 horas
        if horas > 8 or (horas * 2) % 1 != 0:
            raise DatosInvalidosError("horas", horas, "bloques de 0.5 h y maximo 8 horas")
        return True

    def describir(self):
        return f"{self.id} | Asesoria '{self.nombre}' | nivel {self._nivel} | ${self.tarifa_hora:,.0f}/h"
