import json
import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

# Получаем абсолютный путь до текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем путь до файла логов относительно текущей директории
rel_file_path = os.path.join(current_dir, "../logs/services.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def check_cashback(data: List[Dict], month: str, year: str) -> str:
    """
    Анализ выгодных категорий повышенного кэшбэка
    """
    if not data:
        logger.error("Ошибка: Список данных пуст")
        raise ValueError("Список данных пуст")

    category = {}

    start_date = datetime.strptime(f"01.{month}.{year} 00:00:00", "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(f"31.{month}.{year} 23:59:59", "%d.%m.%Y %H:%M:%S")

    logger.info("Фильтрация данных по дате")
    sorted_with_date = [
        dicts
        for dicts in data
        if start_date <= datetime.strptime(dicts["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date
    ]

    if not sorted_with_date:
        logger.error("Ошибка: Указанной даты в данных не существует")
        raise ValueError("Указанной даты в данных не существует")

    logger.info("Фильтрация данных по категории и полученному кэшбэку за месяц")
    for sorted_dicts in sorted_with_date:
        category_name = sorted_dicts["Категория"]
        cashback = sorted_dicts["Кэшбэк"]
        if not pd.isna(cashback):
            if category_name not in category:
                category[category_name] = int(cashback)
            else:
                category[category_name] += int(cashback)
        else:
            continue

    return json.dumps(category, indent=4, ensure_ascii=False)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """Накопление через округления трат"""
    start_time = time.time()
    if limit not in [10, 50, 100]:
        logger.info("Введен неподдерживаемый предел округления")
        end_time = time.time()
        logger.info(f"Время работы функции составило: {end_time - start_time} сек")
        return "Введен неподдерживаемый предел округления"

    if not transactions:
        logger.info("Список данных пуст")
        end_time = time.time()
        logger.info(f"Время работы функции составило: {end_time - start_time} сек")
        return "Список данных пуст"

    else:
        logger.info("Сортируем данные по дате")
        formatted_month = month[5:] + "." + month[:4]
        sorted_by_date = [dicts for dicts in transactions if formatted_month in dicts["Дата операции"]]

        if not sorted_by_date:
            logger.info("Такой даты в данных не нашлось")
            end_time = time.time()
            logger.info(f"Время работы функции составило: {end_time - start_time} сек")
            return "Такой даты в данных не нашлось"

        list_of_amount = [abs(dicts["Сумма операции"]) for dicts in sorted_by_date]
        logger.info(f"Создан список с информацией о сумме операции: {list_of_amount}")

        sums = 0
        for amount in list_of_amount:
            reminder = amount % limit
            if reminder != 0:
                result = limit - reminder
                sums += result
        logger.info(f"Сумма накоплений составила {sums} руб.")

        end_time = time.time()
        logger.info(f"Время работы функции составило: {end_time - start_time} сек")

        return json.dumps(round(sums, 2))


def searching_information(information: str, transaction: List[Dict]) -> str:
    """Поиск информации по запросу с описанием или категорией"""
    if not transaction:
        logger.error("Список данных пуст")
        raise ValueError("Список данных пуст")

    transaction_list = [dicts for dicts in transaction for value in dicts.values() if value == information]

    if not transaction_list:
        logger.error("Информации по запросу не нашлось")
        raise ValueError("Информации по запросу не нашлось")

    logger.info(f"Данные отсортированы: {transaction_list}")
    return json.dumps(transaction_list, indent=4, ensure_ascii=False)


def searching_with_phone_number(transaction: List[Dict]) -> str:
    """Поиск по телефонным номерам. Функция возвращает транзакции с номерами телефонов, содержащихся в описании"""
    if not transaction:
        logger.error("Список данных пуст")
        raise ValueError("Список данных пуст")

    elif not isinstance(transaction, list):
        logger.error("Передан неправильный тип данных. Должен быть список")
        raise ValueError("Передан неправильный тип данных. Должен быть список")

    sorted_list = []
    pattern = re.compile(r"[\w\s]*\+?\d[\s\-]?\(?\d{3}\)?[\s\-]?\d{2}\d?[\s\-]?\d{2}[\s\-]?\d{2}")

    for dicts in transaction:
        description = dicts.get("Описание", "")
        if pattern.search(description):
            logger.info(f"Найдена подходящая строка в соответствии с шаблоном: {description}. Добавляем в список.")
            sorted_list.append(dicts)

    if not sorted_list:
        logger.error("Данных с телефонными номерами в описании не нашлось")
        raise ValueError("Данных с телефонными номерами в описании не нашлось")

    logger.info("Вывод результата")
    return json.dumps(sorted_list, indent=4, ensure_ascii=False)


def searching_for_transactions_to_physical_person(transaction: List[Dict]) -> str:
    """Поиск всех переводов физическим лицам по категории 'Переводы'"""
    if not transaction:
        logger.error("Список данных пуст")
        raise ValueError("Список данных пуст")

    sorted_list = []

    pattern = re.compile(r"\w+\s\w\.")
    for dicts in transaction:
        if dicts["Категория"] == "Переводы":
            logger.info(f"Найдена транзакция категории 'Переводы': {dicts}")
            description = dicts.get("Описание", "")
            if pattern.search(description):
                logger.info(f"Описание '{description}' соответствует шаблону")
                sorted_list.append(dicts)

    if not sorted_list:
        logger.error("Данных с переводами физическим лицам не нашлось")
        raise ValueError("Данных с переводами физическим лицам не нашлось")

    logger.info("Вывод результата")
    return json.dumps(sorted_list, indent=4, ensure_ascii=False)
