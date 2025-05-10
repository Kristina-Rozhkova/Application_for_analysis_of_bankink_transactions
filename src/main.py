import json
from datetime import datetime
import pandas as pd

from src.reports import spending_by_category
from src.services import (check_cashback, investment_bank, searching_for_transactions_to_physical_person,
                          searching_information, searching_with_phone_number)
from src.utils import excel_reading

if __name__ == "__main__":

    def main() -> str:
        while True:
            print("Здравствуйте! \nЖелаете начать работу с приложением?")
            user_input = input()

            if user_input == "нет".lower():
                return "До встречи!"

            if user_input == "да".lower():
                read_file = excel_reading("../data/operations.xlsx")
                while True:
                    print(
                        "Выберите пункт из списка:\n"
                        "1.Анализ выгодных категорий повышенного кэшбэка за месяц\n"
                        "2.Округление Ваших трат до порога 10, 50, 100 руб.\n"
                        "3.Фильтрация данных по запросу.\n"
                        "4.Фильтрация данных по телефонным номерам.\n"
                        "5.Фильтрация данных по переводам физическим лицам.\n"
                        "6.Сформировать отчет по тратам по категориям за последние 3 месяца."
                    )
                    user_choice = input()

                    if user_choice == "1":
                        print("Введите период для анализа выгодных категорий повышенного кэшбэка")
                        user_month = input("Месяц: ")
                        user_year = input("Год: ")

                        cashback = check_cashback(read_file, user_month, user_year)

                        print("Ответ по запросу:")
                        return cashback

                    elif user_choice == "2":
                        print(
                            "Введите месяц, для которого рассчитывается отложенная сумма "
                            '(строка в формате "YYYY-MM")'
                        )
                        user_month_and_year = input()

                        print(
                            "Введите пункт для выбора порога округления трат:\n"
                            "1. 10 руб.\n"
                            "2. 50 руб.\n"
                            "3. 100 руб."
                        )
                        user_limit = input("Пункт № ")

                        if user_limit == "1":
                            investment = investment_bank(user_month_and_year, read_file, 10)
                            return f"Сумма накоплений составила: {investment} руб."

                        elif user_limit == "2":
                            investment = investment_bank(user_month_and_year, read_file, 50)
                            return f"Сумма накоплений составила: {investment} руб."

                        elif user_limit == "3":
                            investment = investment_bank(user_month_and_year, read_file, 100)
                            return f"Сумма накоплений составила: {investment} руб."

                        else:
                            return "Введен неверный номер пункта. Попробуйте снова!"

                    elif user_choice == "3":
                        print("Введите фразу или слово для поиска.")
                        user_information = input()

                        information = searching_information(user_information, read_file)

                        print("Ответ на запрос:")
                        return information

                    elif user_choice == "4":
                        print("Ответ по запросу:")
                        return searching_with_phone_number(read_file)

                    elif user_choice == "5":
                        print("Ответ по запросу:")
                        return searching_for_transactions_to_physical_person(read_file)

                    elif user_choice == "6":
                        print("Введите категорию трат, по которой хотите получить отчет.")
                        user_category = input().title()

                        print("Введите дату, от которой будут отсчитываться последние 3 месяца")
                        user_date = input("Дату введите в формате ДД.ММ.ГГГГ ")

                        result = spending_by_category(pd.DataFrame(read_file), user_category, user_date)
                        # filename = f"report_{datetime.now().strftime('%d%m%Y_%H%M%S')}.json"
                        #
                        # with open(filename, "r", encoding="utf-8") as file:  # type: ignore
                        #     json_data = json.load(file)
                        #     print("Результат отчета:")
                        #     print(json.dumps(json_data, ensure_ascii=False, indent=4))
                        print("Отчет сформирован.")
                        return result

                    else:
                        print(
                            "Вы ввели несуществующий номер пункта\n"
                            'Введите "да", если хотите вернуться к списку, или любое другое слово/символ, если '
                            "хотите завершить работу."
                        )
                        user_continue = input()

                        if user_continue == "да".lower():
                            print("Продолжаем работу...")

                        else:
                            return "До встречи!"
            else:
                print('Введите "да" или "нет".')

    print(main())
