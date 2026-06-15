from data_models import Expense, ExpenseTree


# класс хранит всю логику по бюджету
class BudgetHelper:
    def __init__(self, days_in_month: int = 31):
        # сколько дней считаем в месяце
        self.days_in_month = days_in_month
        # сумма трат по каждому дню
        self.day_totals = [0.0] * (self.days_in_month + 1)
        # префиксные суммы для быстрых запросов по периоду
        self.prefix_sums = [0.0] * (self.days_in_month + 1)
        # сумма по категориям
        self.category_totals = {}
        # стек истории для отмены последней траты
        self.history = []
        # дерево для хранения всех трат
        self.tree = ExpenseTree()

    def add_expense(self, day: int, amount: float, category: str):
        # проверяем день
        if not self._check_day(day):
            return False, 'ошибка день должен быть от 1 до 31'

        # сумма должна быть положительной
        if amount <= 0:
            return False, 'ошибка сумма должна быть больше нуля'

        # убираем лишние пробелы и делаем буквы маленькими
        clean_category = category.strip().lower()
        # создаем объект траты
        expense = Expense(day=day, amount=amount, category=clean_category)

        # кладем трату в стек истории
        self.history.append(expense)
        # увеличиваем сумму по нужному дню
        self.day_totals[day] += amount
        # обновляем сумму по категории
        self.category_totals[clean_category] = self.category_totals.get(clean_category, 0.0) + amount
        # добавляем трату в дерево
        self.tree.insert(expense)
        # пересчитываем префиксные суммы
        self._rebuild_prefix()

        # сообщаем что все прошло хорошо
        return True, 'трата добавлена'

    def sum_for_period(self, day_a: int, day_b: int):
        # проверяем первый день
        if not self._check_day(day_a) or not self._check_day(day_b):
            return False, 0.0, 'ошибка дни должны быть от 1 до 31'

        # начало периода не должно быть больше конца
        if day_a > day_b:
            return False, 0.0, 'ошибка начало периода не может быть больше конца'

        # берем сумму через префиксные суммы за o 1
        total = self.prefix_sums[day_b] - self.prefix_sums[day_a - 1]
        return True, total, ''

    def find_max_day(self):
        # линейный поиск дня с максимальной суммой
        max_day = 1
        max_sum = self.day_totals[1]

        # идем по всем дням и ищем максимум
        for day in range(2, self.days_in_month + 1):
            if self.day_totals[day] > max_sum:
                max_sum = self.day_totals[day]
                max_day = day

        return max_day, max_sum

    def sort_categories_by_sum(self):
        # сортировка вставками по убыванию суммы
        items = list(self.category_totals.items())

        # начинаем со второго элемента
        for i in range(1, len(items)):
            current = items[i]
            j = i - 1

            # двигаем элементы пока находим большие
            while j >= 0 and items[j][1] < current[1]:
                items[j + 1] = items[j]
                j -= 1

            # вставляем текущий элемент на нужное место
            items[j + 1] = current

        return items

    def undo_last(self):
        # стек помогает отменить последнюю добавленную трату
        if not self.history:
            return False, 'нечего отменять'

        # забираем последнюю трату из истории
        last_expense = self.history.pop()
        # уменьшаем сумму в нужном дне
        self.day_totals[last_expense.day] -= last_expense.amount

        # уменьшаем сумму категории
        if last_expense.category in self.category_totals:
            self.category_totals[last_expense.category] -= last_expense.amount
            # если сумма стала нулевой то удаляем категорию
            if self.category_totals[last_expense.category] <= 0:
                del self.category_totals[last_expense.category]

        # дерево строим заново из истории
        self._rebuild_tree_from_history()
        # префиксные суммы тоже строим заново
        self._rebuild_prefix()
        return True, 'последняя трата отменена'

    def get_all_expenses(self):
        # выводим все траты через обход дерева
        return self.tree.inorder()

    def get_total_for_day(self, day: int):
        # проверяем корректность дня
        if not self._check_day(day):
            return False, 0.0
        # возвращаем сумму по дню
        return True, self.day_totals[day]

    def _rebuild_prefix(self):
        # переменная для накопления суммы
        running_sum = 0.0
        # нулевой элемент всегда ноль
        self.prefix_sums[0] = 0.0

        # проходим по всем дням и строим накопительную сумму
        for day in range(1, self.days_in_month + 1):
            running_sum += self.day_totals[day]
            self.prefix_sums[day] = running_sum

    def _rebuild_tree_from_history(self):
        # сначала чистим дерево
        self.tree.clear()
        # потом снова добавляем все траты из истории
        for expense in self.history:
            self.tree.insert(expense)

    def _check_day(self, day: int):
        # день должен быть внутри границ месяца
        return 1 <= day <= self.days_in_month
