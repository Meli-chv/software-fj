# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Curso Programación (213023) — UNAD — Fase 4: Prácticas simuladas
Autora: Anyi Melisa Chaparro Vargas — Grupo 213023A_2204

## Descripción
Aplicación orientada a objetos en Python que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías) y reservas para la empresa
Software FJ. No usa base de datos: la información vive en listas internas y
solo se usa un archivo para registrar eventos y errores (`software_fj.log`).

## Cómo ejecutarlo
```bash
python main.py
```
Requiere Python 3.8 o superior. No necesita librerías externas.

## Estructura
| Archivo | Contenido |
|---|---|
| `entidad.py` | Clase abstracta `Entidad` (base de todo el sistema) |
| `cliente.py` | Clase `Cliente` con validaciones y atributos privados |
| `servicios.py` | Clase abstracta `Servicio` y sus hijas `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `sistema.py` | Clase `SistemaFJ` que maneja las listas internas |
| `excepciones.py` | Excepciones personalizadas |
| `registro.py` | Registro de eventos y errores en el archivo de logs |
| `main.py` | Simulación de más de 10 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `_costo_base`, `validar_parametros` y `describir`.
- **Encapsulación:** los datos del cliente son privados (`__nombre`, `__telefono`…) y se acceden por propiedades con validación; el teléfono se muestra enmascarado.
- **Sobrecarga:** `calcular_costo(horas, impuesto=False, descuento=0.0)` admite cuatro variantes de llamado.
- **Excepciones:** excepciones propias, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from e`.
