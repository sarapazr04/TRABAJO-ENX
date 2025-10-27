"""
Importa datos desde un archivo CSV, Excel o SQLite.

Parámetros
----------
file_path : str
    Ruta al archivo a importar (.csv, .xlsx, .xls, .sqlite, .db).
preview_rows : int, opcional
    Número de filas a mostrar como vista previa (por defecto 5).

Devuelve
--------
(df, preview) : Tuple[pd.DataFrame, pd.DataFrame]
    df -> DataFrame completo cargado.
    preview -> Primeras filas del DataFrame para verificación rápida.

Excepciones
-----------
RuntimeError
    Si el formato del archivo no es válido, está corrupto o no se puede leer.
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Tuple
from .utils import coerce_dtypes


def import_data(file_path: str, preview_rows: int = 5) -> Tuple[pd.DataFrame,
                                                                pd.DataFrame]:

    path = Path(file_path)

    if not path.exists():
        raise RuntimeError(f"El archivo no existe: {file_path}")

    try:
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        elif path.suffix.lower() in [".xls", ".xlsx"]:
            df = pd.read_excel(path)
        elif path.suffix.lower() in [".sqlite", ".db"]:
            with sqlite3.connect(path) as conn:
                tables = pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table';", conn
                )
                if tables.empty:
                    raise RuntimeError("La base de datos no contiene tablas.")
                table_name = tables.iloc[0, 0]
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        else:
            raise RuntimeError(f"Formato de archivo no soportado: {path.suffix}")

        # Conversión de tipos (numéricos, fechas, etc.)
        df = coerce_dtypes(df)

        preview = df.head(preview_rows)
        return df, preview

    except Exception as e:
        raise RuntimeError(f"Error al importar datos ({path.name}): {e}")
