import joblib
import tempfile
from sklearn.linear_model import LinearRegression


def test_model_save_and_load():
    model = LinearRegression()
    model.fit([[1], [2], [3]], [2, 4, 6])

    data = {
        "model": model,
        "desc": "modelo_de_prueba",
        "r2": [1.0, 1.0],
        "mse": [0.0, 0.0],
        "col_entrada": ["x"],
        "col_salida": "y"
    }

    with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
        joblib.dump(data, tmp.name)
        loaded = joblib.load(tmp.name)

    # Validar estructura
    assert "model" in loaded
    assert "r2" in loaded
    assert "mse" in loaded
    assert "col_entrada" in loaded
    assert "col_salida" in loaded

    # Validar que el modelo sigue funcionando
    pred = loaded["model"].predict([[4]])
    assert pred[0] == 8
