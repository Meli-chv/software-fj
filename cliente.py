# cliente.py
# Clase Cliente con validaciones y encapsulacion de los datos personales.

import re
from entidad import Entidad
from excepciones import DatosInvalidosError, ParametroFaltanteError


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    # Expresion regular sencilla para validar correos
    PATRON_CORREO = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"

    def __init__(self, nombre, documento, correo, telefono):
        # Primero reviso que no falte ningun dato
        for campo, valor in (("nombre", nombre), ("documento", documento),
                             ("correo", correo), ("telefono", telefono)):
            if valor is None or str(valor).strip() == "":
                raise ParametroFaltanteError(campo)

        # Uso los setters para que las validaciones se apliquen tambien al crear
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

        # Solo si todo es valido llamo a Entidad para asignar el id
        super().__init__("CLI")

    # ---------- Propiedades (encapsulacion) ----------

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()
        # El nombre solo debe tener letras y espacios, minimo 3 caracteres
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise DatosInvalidosError("nombre", valor, "solo letras y minimo 3 caracteres")
        self.__nombre = valor.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()
        # El documento debe ser numerico y tener entre 6 y 10 digitos
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise DatosInvalidosError("documento", valor, "debe tener entre 6 y 10 digitos")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = str(valor).strip().lower()
        if not re.match(self.PATRON_CORREO, valor):
            raise DatosInvalidosError("correo", valor, "formato de correo no valido")
        self.__correo = valor

    @property
    def telefono(self):
        # Al mostrar el telefono lo oculto parcialmente para proteger el dato
        return "*" * 6 + self.__telefono[-4:]

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        # Telefono colombiano: 10 digitos
        if not valor.isdigit() or len(valor) != 10:
            raise DatosInvalidosError("telefono", valor, "debe tener 10 digitos")
        self.__telefono = valor

    # ---------- Metodos obligatorios de Entidad ----------

    def validar(self):
        # Si el objeto existe, ya paso por los setters, entonces es valido
        return True

    def describir(self):
        return f"{self.id} | {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
