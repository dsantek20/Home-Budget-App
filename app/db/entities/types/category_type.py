from enum import Enum


class CategoryType(str, Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"