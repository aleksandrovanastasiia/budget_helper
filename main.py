from budget_manager import BudgetHelper


# показываем меню на экране
def show_menu():
    print()
    print("========================================")
    print("           Бюджетный помощник           ")
    print("========================================")
    print("1. Добавить расход")
    print("2. Посчитать сумму за период")
    print("3. Найти день с максимальным расходом")
    print("4. Показать категории по сумме")
    print("5. Отменить последнюю трату")
    print("6. Показать все траты")
    print("7. Показать сумму за день")
    print("0. Выход")
    print("========================================")
    print()


# читаем целое число пока пользователь не введет правильно
def read_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Введите целое число")


# читаем дробное число пока пользователь не введет правильно
def read_float(text):
    while True:
        try:
            return float(input(text).replace(",", "."))
        except ValueError:
            print("Введите корректную сумму")


# главная функция программы
def main():
    # создаем объект для работы с бюджетом
    app = BudgetHelper()

    # запускаем программу пока пользователь не выйдет
    while True:
        show_menu()
        choice = input("Введите команду: ").strip()

        if choice == "1":
            day = read_int("Введите день от 1 до 31: ")
            amount = read_float("Введите сумму расхода: ")
            category = input("Введите категорию: ").strip()
            ok, message = app.add_expense(day, amount, category)
            print(message)

        elif choice == "2":
            a = read_int("Введите начальный день: ")
            b = read_int("Введите конечный день: ")
            ok, total, message = app.sum_for_period(a, b)
            if ok:
                print(f"Сумма расходов за период: {total:.2f}")
            else:
                print(message)

        elif choice == "3":
            day, total = app.find_max_day()
            print(f"День с максимальным расходом: {day}")
            print(f"Сумма расходов: {total:.2f}")

        elif choice == "4":
            items = app.sort_categories_by_sum()
            if not items:
                print("Категории пока отсутствуют")
            else:
                print("Категории по сумме расходов")
                for category, total in items:
                    print(f"{category} - {total:.2f}")

        elif choice == "5":
            ok, message = app.undo_last()
            print(message)

        elif choice == "6":
            expenses = app.get_all_expenses()
            if not expenses:
                print("Список расходов пуст")
            else:
                print("Все добавленные расходы")
                for expense in expenses:
                    print(f"День {expense.day} Сумма {expense.amount:.2f} Категория {expense.category}")

        elif choice == "7":
            day = read_int("Введите день: ")
            ok, total = app.get_total_for_day(day)
            if ok:
                print(f"Сумма расходов за день {day}: {total:.2f}")
            else:
                print("Ошибка. День должен быть от 1 до 31")

        elif choice == "0":
            print("Работа программы завершена")
            break

        else:
            print("Неверная команда")


if __name__ == "__main__":
    main()
