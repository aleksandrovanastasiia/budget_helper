from dataclasses import dataclass


# это простая модель одной траты
@dataclass
class Expense:
    # день месяца
    day: int
    # сумма траты
    amount: float
    # категория траты
    category: str


# узел дерева для хранения трат по дням
class TreeNode:
    def __init__(self, expense: Expense):
        # в узле хранится сам день
        self.day = expense.day
        # список трат на этот день
        self.expenses = [expense]
        # левая ветка дерева
        self.left = None
        # правая ветка дерева
        self.right = None


# дерево для хранения всех трат
class ExpenseTree:
    def __init__(self):
        # корень дерева сначала пустой
        self.root = None

    def insert(self, expense: Expense):
        # добавляем трату в дерево
        self.root = self._insert(self.root, expense)

    def _insert(self, node, expense: Expense):
        # если узла нет то создаем новый
        if node is None:
            return TreeNode(expense)

        # если день меньше то идем влево
        if expense.day < node.day:
            node.left = self._insert(node.left, expense)
        # если день больше то идем вправо
        elif expense.day > node.day:
            node.right = self._insert(node.right, expense)
        # если день одинаковый то просто добавляем в список
        else:
            node.expenses.append(expense)

        # возвращаем текущий узел обратно
        return node

    def inorder(self):
        # этот обход нужен чтобы вывести траты по порядку дней
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        # если узел пустой то просто выходим
        if node is None:
            return

        # сначала идем в левую часть дерева
        self._inorder(node.left, result)
        # потом добавляем траты текущего дня
        result.extend(node.expenses)
        # потом идем в правую часть дерева
        self._inorder(node.right, result)

    def clear(self):
        # очищаем дерево полностью
        self.root = None
