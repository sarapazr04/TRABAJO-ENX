"""
Paquete data_import
-------------------
Módulo encargado de la importación y previsualización de datos desde diferentes formatos:
CSV, Excel y SQLite.

Módulos:
- importer.py: lógica principal de carga y validación de archivos.
- utils.py: funciones auxiliares para detección y conversión de tipos de datos.

Funciones principales expuestas:
- import_data(file_path: str, preview_rows: int = 5)
"""

from importer import import_data
from utils import coerce_dtypes

__all__ = ["import_data", "coerce_dtypes"]
