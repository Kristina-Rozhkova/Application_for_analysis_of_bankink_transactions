from unittest.mock import patch

import pandas as pd

from src.utils import excel_reading


@patch("pandas.read_excel")
def test_excel_reading(mock_read_excel):
    """Тестирование чтения excel-файла"""
    mock_data = [
        {
            "Дата операции": "03.01.2018 15:03:35",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -73.06,
            "Валюта операции": "RUB",
            "Сумма платежа": -73.06,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Супермаркеты",
            "MCC": 5499.0,
            "Описание": "Magazin 25",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 73.06,
        },
        {
            "Дата операции": "03.01.2018 14:55:21",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -21.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 21.0,
        },
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
        {
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Номер карты": "nan",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        },
    ]

    mock_df = pd.DataFrame(mock_data)
    mock_read_excel.return_value = mock_df

    result = excel_reading("../data/operations.xlsx")

    assert result == mock_read_excel.return_value.to_dict(orient="records")
    mock_read_excel.assert_called_once_with("../data/operations.xlsx", engine="openpyxl")


@patch("pandas.read_excel")
def test_excel_reading_file_not_found(mock_read_excel):
    """Тестирование случая с ненайденным файлом"""
    mock_read_excel.side_effect = FileNotFoundError("Файл по указанному пути не найден")

    result = excel_reading("../data/nonexistent_file.xlsx")

    assert result == []
    mock_read_excel.assert_called_once_with("../data/nonexistent_file.xlsx", engine="openpyxl")


@patch("pandas.read_excel")
def test_excel_reading_exception(mock_read_excel):
    """Тестирование случая с общим исключением (любой другой ошибкой)"""
    mock_read_excel.side_effect = Exception("Произошла ошибка")

    result = excel_reading("../data/file.xlsx")

    assert result == []
    mock_read_excel.assert_called_once_with("../data/file.xlsx", engine="openpyxl")
