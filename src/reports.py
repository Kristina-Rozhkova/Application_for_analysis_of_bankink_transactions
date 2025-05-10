import logging
import os
import re
from datetime import datetime
from functools import wraps
from typing import Any, Optional

import pandas as pd

# Получаем абсолютный путь до текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем путь до файла логов относительно текущей директории
rel_file_path = os.path.join(current_dir, "../logs/reports.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report(init_filename: Optional[str] = None) -> Any:
    """Декоратор, который записывает результат функции-отчета в файл"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            filename = init_filename if init_filename else f"report_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"
            filename = str(filename)
            with open(filename, "w", encoding="utf-8") as file:
                result.to_json(file, orient="records", force_ascii=False, indent=4)

            return result

        return wrapper

    return decorator


@report()
def spending_by_category(transactions: pd.DataFrame, category: str, dates: Optional[str] = None) -> pd.DataFrame:
    """Траты по категориям за последние 3 месяца"""
    list_transactions = transactions.to_dict(orient="records")

    if not dates:
        logger.info("Дата в качестве аргумента не передана, генерируем текущую дату.")
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d.%m.%Y %H:%M:%S")

    else:
        logger.info("Дата в качестве аргумента передана, проверяем ее соответствие необходимому формату")
        pattern = r"^\d{2}\.\d{2}\.\d{4}$"
        checking = re.match(pattern, dates)
        if checking:
            formatted_date = dates + " 23:59:59"
        else:
            logger.error("Введен неверный формат даты")
            raise ValueError("Введен неверный формат даты")

    end_date = datetime.strptime(formatted_date, "%d.%m.%Y %H:%M:%S")

    if end_date.month >= 4:
        start_date = end_date.replace(month=end_date.month - 3)
    else:
        start_date = end_date.replace(month=end_date.month + 9, year=end_date.year - 1)

    logger.info("Сортировка данных по дате")
    sorted_by_date = [
        dicts
        for dicts in list_transactions
        if start_date <= datetime.strptime(dicts["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date
    ]

    logger.info("Сортировка данных по категории")
    sorted_transactions = [dicts for dicts in sorted_by_date if dicts["Категория"] == category]
    if not sorted_transactions:
        logger.error("Категории по запросу в данных не нашлось")
        raise ValueError("Категории по запросу в данных не нашлось")

    return pd.DataFrame(sorted_transactions)


# trans = [
#     {
#         "Дата операции": "03.01.2018 15:03:35",
#         "Дата платежа": "04.01.2018",
#         "Номер карты": "*7197",
#         "Статус": "OK",
#         "Сумма операции": -73.06,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -73.06,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": 35,
#         "Категория": "Супермаркеты",
#         "MCC": 5499.0,
#         "Описание": "Magazin 25",
#         "Бонусы (включая кэшбэк)": 1,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 73.06,
#     },
#     {
#         "Дата операции": "13.01.2025 08:55:21",
#         "Дата платежа": "05.01.2018",
#         "Номер карты": "*7197",
#         "Статус": "OK",
#         "Сумма операции": -21.0,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -21.0,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": "nan",
#         "Категория": "Красота",
#         "MCC": 5977.0,
#         "Описание": "OOO Balid",
#         "Бонусы (включая кэшбэк)": 0,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 21.0,
#     },
#     {
#         "Дата операции": "01.01.2018 20:27:51",
#         "Дата платежа": "04.01.2018",
#         "Номер карты": "*7197",
#         "Статус": "OK",
#         "Сумма операции": -316.0,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -316.0,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": "nan",
#         "Категория": "Красота",
#         "MCC": 5977.0,
#         "Описание": "OOO Balid",
#         "Бонусы (включая кэшбэк)": 6,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 316.0,
#     },
#     {
#         "Дата операции": "01.01.2018 12:49:53",
#         "Дата платежа": "01.01.2018",
#         "Номер карты": "nan",
#         "Статус": "OK",
#         "Сумма операции": -3000.0,
#         "Валюта операции": "RUB",
#         "Сумма платежа": -3000.0,
#         "Валюта платежа": "RUB",
#         "Кэшбэк": "nan",
#         "Категория": "Переводы",
#         "MCC": "nan",
#         "Описание": "Линзомат ТЦ Юность",
#         "Бонусы (включая кэшбэк)": 0,
#         "Округление на инвесткопилку": 0,
#         "Сумма операции с округлением": 3000.0,
#     },
# ]
# print(spending_by_category(pd.DataFrame(trans), "Переводы", "01.01.2018"))
