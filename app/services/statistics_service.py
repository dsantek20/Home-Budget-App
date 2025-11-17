
from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import Annotated, List, Optional
from fastapi import Depends
from api.models.statistics_models import Categories, CategoryAggregate, CategoryBreakdown, ExpenseSummary, FinancialOverview, IncomeSummary, TransactionSummary
from db.entities.income_entities import Income
from db.entities.expense_entities import Expense
from utils.datetime_helpers import get_current_date, get_past_date
from db.dao.statistics_dao import StatisticsDao, StatisticsDaoInstance
from db.entities.user_entities import User



class StatisticsService:
    def __init__(self, dao: StatisticsDao):
        self.dao = dao

    def _get_date_range(self, period: Optional[str] = None) -> Optional[date]:
        if not period:
            return None
        
        if period == "week":
            start_date = get_past_date(days=7)
        elif period == "month":
            start_date = get_past_date(days=30)
        elif period == "quarter":
            start_date = get_past_date(days=90)
        elif period == "year":
            start_date = get_past_date(days=365)
        else:
            return None
        
        return start_date
    
    def _group_expenses_by_category(self, expenses: List[Expense]) -> Categories:
        by_category: Categories = defaultdict(CategoryAggregate)

        for exp in expenses:
            data = by_category[exp.category.name]

            data.total += exp.amount
            data.count += 1
            data.transactions.append(
                TransactionSummary(
                    id=str(exp.id),
                    amount=float(exp.amount),
                    description=exp.description,
                    date=exp.expense_date.isoformat()
                )
            )

        return by_category
    
    def _group_incomes_by_category(self, incomes: List[Income]) -> Categories:
        by_category: Categories = defaultdict(CategoryAggregate)

        for income in incomes:
            data = by_category[income.category.name]

            data.total += income.amount
            data.count += 1
            data.transactions.append(
                TransactionSummary(
                    id=str(income.id),
                    amount=float(income.amount),
                    description=income.description,
                    date=income.income_date.isoformat()
                )
            )

        return by_category
    
    def _build_category_breakdown(self, by_category: Categories, total_spent: Decimal) -> List[CategoryBreakdown]:
        categories = [
            CategoryBreakdown(
                category=cat,
                total=float(data.total),        
                count=data.count,  
                percentage=float((data.total / total_spent * 100)) if total_spent else 0,
                average=float(data.total / data.count) if data.count > 0 else 0,
                transactions=data.transactions
            )
            for cat, data in by_category.items()
        ]

        categories.sort(key=lambda c: c.total, reverse=True)
        return categories

    async def get_expense_summary(self, user: User, period: Optional[str] = None) -> ExpenseSummary:
        start_date = self._get_date_range(period)
        expenses = await self.dao.get_expenses(user.id, start_date)
        total_spent = sum(exp.amount for exp in expenses)
        
        by_category = self._group_expenses_by_category(expenses)
        categories = self._build_category_breakdown(by_category, total_spent)

        return ExpenseSummary(
            period=period or "all_time",
            total_spent=float(total_spent),
            expense_count=len(expenses),
            average_expense=float(total_spent / len(expenses)) if expenses else 0,
            categories=categories,
            start_date=start_date.isoformat() if start_date else None,
            end_date=get_current_date().isoformat()
        )

    async def get_income_summary(self, user: User, period: Optional[str] = None) -> IncomeSummary:
        start_date = self._get_date_range(period)
        incomes = await self.dao.get_incomes(user.id, start_date)
        total_spent = sum(income.amount for income in incomes)
        
        by_category = self._group_incomes_by_category(incomes)
        categories = self._build_category_breakdown(by_category, total_spent)

        return IncomeSummary(
            period=period or "all_time",
            total_income=float(total_spent),
            income_count=len(incomes),
            average_income=float(total_spent / len(incomes)) if incomes else 0,
            categories=categories,
            start_date=start_date.isoformat() if start_date else None,
            end_date=get_current_date().isoformat()
        )

    async def get_financial_overview(self, user: User, period: Optional[str] = None) -> FinancialOverview:
        start_date = self._get_date_range(period)
        
        incomes = await self.dao.get_incomes(user.id, start_date)
        expenses = await self.dao.get_expenses(user.id, start_date)
        
        total_income = sum(income.amount for income in incomes)
        total_expenses = sum(exp.amount for exp in expenses)
        net_balance = total_income - total_expenses
        
        current_balance = user.balance
        
        return FinancialOverview(
            period=period or "all_time",
            total_income=float(total_income),
            total_expenses=float(total_expenses),
            net_balance=float(net_balance),
            current_account_balance=float(current_balance),
            start_date=start_date.isoformat() if start_date else None,
            end_date=get_current_date().isoformat()
        )


def get_statistics_service(dao: StatisticsDaoInstance) -> StatisticsService:
    return StatisticsService(dao)


StatisticsServiceInstance = Annotated[StatisticsService, Depends(get_statistics_service)]
