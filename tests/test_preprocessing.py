import pandas as pd
import pytest
from GUI.selection_columns import PreprocessingPanel
from GUI import selection_columns


# ============================================================
# MOCK PARA NotificationWindow (evita crear ventanas reales)
# ============================================================

class FakeNotificationWindow:
    def __init__(self, *args, **kwargs):
        pass


@pytest.fixture(autouse=True)
def patch_notification_window(monkeypatch):
    monkeypatch.setattr(selection_columns, "NotificationWindow", FakeNotificationWindow)


# ============================================================
# MOCK PARA stats_label (evita usar elementos GUI reales)
# ============================================================

class FakeLabel:
    def configure(self, **kwargs):
        # No hace nada, solo evita errores
        pass


# ============================================================
# APP Y PANEL FALSOS
# ============================================================

class DummyApp:
    def __init__(self):
        self.preprocessed_df = None
        self.current_dataframe = None

    def set_preprocessed_df(self, df):
        self.preprocessed_df = df

    def _display_data(self, df):
        pass

    def _update_statistics(self, df):
        pass


class DummySelectionPanel:
    def __init__(self, df):
        self.df = df


# ============================================================
# FUNCIÓN AUXILIAR PARA EJECUTAR PREPROCESADO SIN GUI
# ============================================================

def run_preprocessing(option, df, selected_cols, constant=None):
    app = DummyApp()
    panel = DummySelectionPanel(df.copy())
    pre = PreprocessingPanel(None, selected_cols, app, panel)

    # ---- Mock: stats_label necesario para evitar error ----
    pre.stats_label = FakeLabel()

    # ---- Mock variables ----
    pre.option_var = type("obj", (), {"get": lambda self=option: option})

    if constant is not None:
        pre.constant_entry = type("obj", (), {"get": lambda self=constant: constant})
    else:
        pre.constant_entry = type("obj", (), {"get": lambda self="": ""})

    # Ejecutar lógica real
    pre._apply_preprocessing_logic(option)

    return app.preprocessed_df


# ============================================================
#                       TESTS
# ============================================================

def test_preprocessing_drop_rows():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": [4, 5, None]
    })

    new_df = run_preprocessing("drop", df, ["a", "b"])
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
    expected_median = 5

    assert new_df["a"].iloc[1] == expected_median


def test_preprocessing_fill_constant():
    df = pd.DataFrame({
        "a": [None, 2, None]
    })

    new_df = run_preprocessing("constant", df, ["a"], constant="99")

    assert new_df["a"].iloc[0] == 99
    assert new_df["a"].iloc[2] == 99
