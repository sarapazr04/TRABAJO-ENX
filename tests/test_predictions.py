from sklearn.linear_model import LinearRegression
from GUI.predict_model import predict_result


def test_linear_prediction_logic():
    model = LinearRegression()
    model.fit([[1], [2], [3]], [2, 4, 6])

    pred = model.predict([[4]])[0]
    assert abs(pred - 8) < 1e-6


def test_predict_result_function():
    cols = ["x", "y"]
    vals = ["3", "7"]
    formula = "z = x + y"

    result = predict_result(cols, vals, formula)
    assert result == "z = 10"
