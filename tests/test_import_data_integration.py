import pandas as pd
from src.data_import.importer import import_data


def test_import_simple_csv(tmp_path):
    file = tmp_path / "simple.csv"
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df.to_csv(file, index=False)

    df_loaded, preview = import_data(str(file))

    assert len(df_loaded) == 2
    assert list(df_loaded.columns) == ["a", "b"]
