import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Caja negra funcional test para la creación y evaluación de un modelo de regresión lineal

def test_model_creation():
    # Dataset simple
    df = pd.DataFrame({
        "x1": [1, 2, 3, 4, 5],
        "y":  [2, 4, 6, 8, 10]
    })

    X = df[["x1"]]
    y = df["y"]

    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)

    # R² perfecto
    assert r2_score(y, preds) == 1.0
    # ECM perfecto
    assert mean_squared_error(y, preds) == 0.0
