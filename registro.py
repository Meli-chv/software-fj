# registro.py
# Modulo para guardar los eventos y errores en un archivo de logs.
# Uso el modulo logging de Python porque ya trae formato de fecha y niveles.

import logging

# Nombre del archivo donde quedan todos los registros
ARCHIVO_LOG = "software_fj.log"

# Creo un logger propio para el sistema
logger = logging.getLogger("SoftwareFJ")
# Nivel INFO para que guarde tanto eventos normales como errores
logger.setLevel(logging.INFO)

# Solo agrego el manejador una vez (por si el modulo se importa varias veces)
if not logger.handlers:
    # FileHandler escribe en el archivo; encoding utf-8 para las tildes
    manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
    # Formato: fecha | nivel | mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Guarda un evento normal (algo que salio bien)."""
    logger.info(mensaje)


def registrar_error(error, contexto=""):
    """Guarda un error. Si el error viene encadenado, tambien guarda la causa original."""
    texto = f"{contexto} -> {error}" if contexto else str(error)
    # __cause__ tiene la excepcion original cuando se usa 'raise ... from ...'
    if error.__cause__ is not None:
        texto += f" | Causa original: {type(error.__cause__).__name__}: {error.__cause__}"
    logger.error(texto)
