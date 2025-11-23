import pytest
from GUI.predict_model import predict_result


def test_predict_invalid_formula():
    cols = ["x"]
    vals = ["5"]
    formula = "z = x + desconocida"

    with pytest.raises(Exception):
        predict_result(cols, vals, formula)
