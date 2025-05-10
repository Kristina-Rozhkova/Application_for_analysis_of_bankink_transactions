from typing import List

import pandas as pd


def excel_reading(excel_path: str) -> List:
    """Вывод данных из excel-файла"""
    try:
        excel_return = pd.read_excel(excel_path, engine="openpyxl")
        return excel_return.to_dict(orient="records")
    except FileNotFoundError:
        print("Файл по указанному пути не найден")
        return []
    except Exception:
        return []
