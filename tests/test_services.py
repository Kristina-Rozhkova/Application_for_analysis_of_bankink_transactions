import json

import numpy as np
import pytest

from src.services import (check_cashback, investment_bank, searching_for_transactions_to_physical_person,
                          searching_information, searching_with_phone_number)


def test_check_cashback(data_list):
    """Тестирование вывода кэшбэка за выбранный период"""
    result = check_cashback(data_list, "1", "2018")
    data = {"Супермаркеты": 35}
    assert result == json.dumps(data, indent=4, ensure_ascii=False)


def test_check_cashback_wrong_data(data_list):
    """Тестирование работы функции, когда указанной даты в данных нет"""
    with pytest.raises(ValueError) as ex:
        check_cashback(data_list, "12", "2018")
    assert str(ex.value) == "Указанной даты в данных не существует"


def test_check_cashback_clear_data():
    """Тестирование работы функции при работе с пустыми данными"""
    clear_data = []

    with pytest.raises(ValueError) as ex:
        check_cashback(clear_data, "1", "2018")
    assert str(ex.value) == "Список данных пуст"


def test_investment_bank_success(data_list_for_investment_bank):
    """Тестирование успешной работы функции"""
    result_1 = investment_bank("2018-01", data_list_for_investment_bank, 10)
    assert result_1 == "19.94"

    result_2 = investment_bank("2018-01", data_list_for_investment_bank, 50)
    assert result_2 == "89.94"

    result_3 = investment_bank("2018-01", data_list_for_investment_bank, 100)
    assert result_3 == "189.94"


def test_investment_bank_incorrect_limit(data_list_for_investment_bank):
    result = investment_bank("2018-01", data_list_for_investment_bank, 20)
    assert result == "Введен неподдерживаемый предел округления"


def test_investment_bank_incorrect_date(data_list_for_investment_bank):
    result = investment_bank("2020-01", data_list_for_investment_bank, 50)
    assert result == "Такой даты в данных не нашлось"


def test_investment_bank_clear_data_list():
    result = investment_bank("2018-01", [], 100)
    assert result == "Список данных пуст"


def test_searching_information_category(data_list):
    result = searching_information("Супермаркеты", data_list)
    return_data = [
        {
            "Дата операции": "03.01.2018 15:03:35",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -73.06,
            "Валюта операции": "RUB",
            "Сумма платежа": -73.06,
            "Валюта платежа": "RUB",
            "Кэшбэк": 35,
            "Категория": "Супермаркеты",
            "MCC": 5499.0,
            "Описание": "Magazin 25",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 73.06,
        }
    ]
    assert result == json.dumps(return_data, indent=4, ensure_ascii=False)


def test_searching_information_description(data_list):
    result = searching_information("OOO Balid", data_list)
    return_data = [
        {
            "Дата операции": "03.01.2018 14:55:21",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -21.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": np.nan,
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
            "Кэшбэк": np.nan,
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
    ]
    assert result == json.dumps(return_data, indent=4, ensure_ascii=False)


def test_searching_information_error(data_list):
    with pytest.raises(ValueError) as ex:
        searching_information("Поиск", data_list)
    assert str(ex.value) == "Информации по запросу не нашлось"


def test_searching_information_clear_transaction():
    with pytest.raises(ValueError) as ex:
        searching_information("Супермаркеты", [])
    assert str(ex.value) == "Список данных пуст"


def test_searching_with_phone_number_success(data_list_for_searching_with_phone_number):
    result = searching_with_phone_number(data_list_for_searching_with_phone_number)
    data = [
        {
            "Дата операции": "2018-01-03",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -73.06,
            "Валюта операции": "RUB",
            "Сумма платежа": -73.06,
            "Валюта платежа": "RUB",
            "Кэшбэк": 35,
            "Категория": "Супермаркеты",
            "MCC": 5499.0,
            "Описание": "Я МТС +7 921 11-22-33",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 73.06,
        },
        {
            "Дата операции": "2018-01-03",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -21.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": np.nan,
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "Тинькофф Мобайл +7 995 555-55-55",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 21.0,
        },
        {
            "Дата операции": "2018-01-01",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": np.nan,
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "МТС Mobile +7 981 333-44-55",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
    ]
    assert result == json.dumps(data, indent=4, ensure_ascii=False)


def test_searching_with_phone_number_clear_list():
    with pytest.raises(ValueError) as ex:
        searching_with_phone_number([])
    assert str(ex.value) == "Список данных пуст"


def test_searching_with_phone_number_error(data_list):
    with pytest.raises(ValueError) as ex:
        searching_with_phone_number(data_list)
    assert str(ex.value) == "Данных с телефонными номерами в описании не нашлось"


def test_searching_with_phone_number_not_list():
    with pytest.raises(ValueError) as ex:
        searching_with_phone_number({"Описание": "Описание"})
    assert str(ex.value) == "Передан неправильный тип данных. Должен быть список"


def test_searching_for_transactions_to_physical_person_success(data_with_physical_persons):
    result = searching_for_transactions_to_physical_person(data_with_physical_persons)
    data = [
        {
            "Дата операции": "2018-02-03",
            "Дата платежа": "01.01.2018",
            "Номер карты": np.nan,
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": np.nan,
            "Категория": "Переводы",
            "MCC": np.nan,
            "Описание": "Валерий А.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        }
    ]
    assert result == json.dumps(data, indent=4, ensure_ascii=False)


def test_searching_for_transactions_to_physical_person_error(data_list):
    with pytest.raises(ValueError) as ex:
        searching_for_transactions_to_physical_person(data_list)
    assert str(ex.value) == "Данных с переводами физическим лицам не нашлось"


def test_searching_for_transactions_to_physical_person_clear_list():
    with pytest.raises(ValueError) as ex:
        searching_for_transactions_to_physical_person([])
    assert str(ex.value) == "Список данных пуст"
