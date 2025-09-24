# jamasata
Gestor de Contraseñas Seguro

## Descripción
Este proyecto es una aplicación de escritorio en Python usando PyQt5 para gestionar contraseñas seguras.

Crear apunte de contraseñas, posibilidad de registrar nuevas contraseñas asociadas a un servicio e usuario.

Listar apunte de contraseñas, sin mostrar la contraseña en texto claro a menos que el usuario lo requiera.

Editar apunte de contraseñas, permitir la modificación de contraseñas previamente guardadas

Eliminar apunte de contraseñas.

Guardar apuntes de contraseñas cifradas en disco en un archivo JSON con contenido cifrado.

Flujo de clave maestra: el usuario debe establecer una clave maestra en el primer uso; esa clave desbloquea los datos cifrados.


## Requisitos
- Python 3.10.4+
- PyQt5 5.15.2+

Instalar:
```bash
pip install PyQt5
pip install PySide2
pip install pyqt5-tools
pip install argon2-cffi
pip install cryptography
```

## Uso
Ejecutar la aplicación principal:
```bash
python jamasata.py
```

## Notas
- La columna de contraseña en la tabla está oculta para seguridad, pero se puede visualizar al seleccionar un apunte.
- Al iniciar la aplicación por primera vez, es obligatorio crear una **clave maestra**.
  Esta clave se utilizará para proteger y cifrar todas las contraseñas almacenadas en la aplicación.

## Licencia
Propietario: Todos los derechos reservados.

