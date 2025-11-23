import pandas as pd
import sqlite3
import pytest
from data_import.importer import import_data


def test_import_csv_success(tmp_path):
    file = tmp_path / "sample.csv"
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df.to_csv(file, index=False)

    df_loaded, preview = import_data(str(file))

    assert len(df_loaded) == 3
    assert list(df_loaded.columns) == ["a", "b"]
    assert len(preview) <= 5


def test_import_excel_success(tmp_path):
    file = tmp_path / "sample.xlsx"
    df = pd.DataFrame({"x": [10, 20], "y": [30, 40]})
    df.to_excel(file, index=False)

    df_loaded, preview = import_data(str(file))

    assert len(df_loaded) == 2
    assert "x" in df_loaded.columns
    assert "y" in df_loaded.columns


def test_import_sqlite_success(tmp_path):
    file = tmp_path / "db.sqlite"

    # Crear DB con tabla para la prueba
    conn = sqlite3.connect(file)
    df = pd.DataFrame({"c": [1, 2], "d": [3, 4]})
    df.to_sql("tabla", conn, index=False)
    conn.close()

    df_loaded, preview = import_data(str(file))

    assert len(df_loaded) == 2
    assert "c" in df_loaded.columns


def test_import_missing_file():
    with pytest.raises(RuntimeError):
        import_data("archivo_que_no_existe.csv")


def test_import_wrong_extension(tmp_path):
    file = tmp_path / "archivo.txt"
    file.write_text("contenido")

    with pytest.raises(RuntimeError):
        import_data(str(file))


def test_import_type_conversion(tmp_path):
    file = tmp_path / "types.csv"
    df = pd.DataFrame({
        "num": ["1", "2", "3"],
        "date": ["2020-01-01", "2020-01-02", "no_date"]
    })
    df.to_csv(file, index=False)

    df_loaded, _ = import_data(str(file))

    # num debe convertirse a numérico
    assert df_loaded["num"].dtype != object

    # date debería convertirse a datetime porque 2/3 son fechas
    assert "datetime64" in str(df_loaded["date"].dtype)
