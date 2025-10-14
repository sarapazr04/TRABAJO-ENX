from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from data_import.importer import import_data

BASE_DIR = Path(__file__).resolve().parents[2]  
DATA_DIR = BASE_DIR / "data" / "raw"

FILES = [
    DATA_DIR / "housing.csv",
    DATA_DIR / "housing.xlsx",
    DATA_DIR / "housing.db",
]

for file_path in FILES:
    print(f"\nProbando importación de: {file_path}")
    try:
        df, preview = import_data(str(file_path))
        print("Carga correcta. Vista previa:")
        print(preview)
    except Exception as e:
        print("Error:", e)
