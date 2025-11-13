"""
Función auxiliar para el módulo 'data_import'.

Es utilizado para convertir automáticamente columnas de un DataFrame
 a tipos adecuados (numéricos o fechas), garantizando la
 consistencia de los datos importados.
"""


import pandas as pd


def coerce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        # Intentar convertir a numérico
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception:
            pass

        # Intentar convertir a fecha si parece texto
        if (df[col].dtype == "object" or
                str(df[col].dtype).startswith("string")):
            parsed = pd.to_datetime(df[col], errors="coerce")
            # Si al menos el 70% son fechas válidas,
            # la columna se considera temporal
            if parsed.notna().sum() >= len(df) * 0.7:
                df[col] = parsed

    return df
