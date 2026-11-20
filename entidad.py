# entidad.py
# Clase abstracta que representa cualquier entidad general del sistema
# (clientes, servicios y reservas heredan de aqui).

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase base abstracta: no se puede instanciar directamente."""

    # Diccionario de contadores, uno por cada tipo (CLI, SRV, RES)
    _contadores = {}

    def __init__(self, prefijo):
        # Aumento el contador del tipo correspondiente
        Entidad._contadores[prefijo] = Entidad._contadores.get(prefijo, 0) + 1
        # El id queda como por ejemplo CLI-001, SRV-001, RES-001
        self._id = f"{prefijo}-{Entidad._contadores[prefijo]:03d}"
        # Guardo la fecha en que se creo el objeto
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        # Solo lectura: el id no se puede cambiar desde afuera
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Cada clase hija debe decir como se describe a si misma."""
        pass

    @abstractmethod
    def validar(self):
        """Cada clase hija debe implementar sus propias validaciones."""
        pass

    def __str__(self):
        # Por defecto, imprimir el objeto muestra su descripcion
        return self.describir()
