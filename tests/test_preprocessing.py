import pandas as pd
import numpy as np
from GUI.selection_columns import PreprocessingPanel


class DummyApp:
    """Simula la app sin GUI, solo para almacenar el resultado."""
    def __init__(self):
        self.preprocessed_df = None
    
    def set_preprocessed_df(self, df):
        self.preprocessed_df = df
        

class DummySelectionPanel:
    """Simula el panel con el DataFrame original."""
    def __init__(self, df):
        self.df = df


def run_preprocessing(option, df, selected_cols, constant=None):
    """Ejecuta la lógica interna del preprocesado (sin GUI)."""
    app = DummyApp()
    panel = DummySelectionPanel(df.copy())
    pre = PreprocessingPanel(None, selected_cols, app, panel)

    # Asignar opción manualmente
    pre.option_var = type("obj", (), {"get": lambda self=option: option})

    if constant is not None:
        pre.constant_entry = type("obj", (), {"get": lambda self=constant: constant})
    else:
        pre.constant_entry = type("obj", (), {"get": lambda self="": ""})

    # Simular llamada al thread → llamamos directamente a la función correcta
    pre._apply_preprocessing_logic(option)
    
    return app.preprocessed_df


# ---------------------- PRUEBAS ----------------------


def test_preprocessing_drop_rows():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": [4, 5, None]
    })

    new_df = run_preprocessing("drop", df, ["a", "b"])

    # Solo la fila 0 queda completa
    assert len(new_df) == 1
    assert new_df.iloc[0]["a"] == 1


def test_preprocessing_fill_mean():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": [10, 20, 30]
    })

    new_df = run_preprocessing("mean", df, ["a"])

    expected_mean = (1 + 3) / 2
    assert new_df["a"].iloc[1] == expected_mean


def test_preprocessing_fill_median():
    df = pd.DataFrame({
        "a": [1, None, 9],
        "b": [0, 0, 0]
    })

    new_df = run_preprocessing("median", df, ["a"])

    expected_median = 5  # mediana de [1,9]
    assert new_df["a"].iloc[1] == expected_median


def test_preprocessing_fill_constant():
    df = pd.DataFrame({
        "a": [None, 2, None]
    })

    new_df = run_preprocessing("constant", df, ["a"], constant="99")

    assert new_df["a"].iloc[0] == 99
    assert new_df["a"].iloc[2] == 99
