from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models.base import Budget, Category, Transaction


class ExpenseRepository:
    def __init__(self, session: Session | None = None):
        self.session = session or Session(bind=engine)

    def add_transaction(self, description: str, amount: float, date: str, category_name: str | None = None) -> Transaction:
        category = self._get_or_create_category(category_name or "uncategorized")
        transaction = Transaction(
            description=description,
            amount=amount,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            category=category,
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def list_transactions(self) -> List[Transaction]:
        return list(self.session.scalars(select(Transaction).order_by(Transaction.date.desc())).all())

    def get_summary(self) -> dict:
        transactions = self.list_transactions()
        total_spending = sum(float(tx.amount) for tx in transactions if float(tx.amount) > 0)
        monthly_summary = {}
        category_summary = {}
        for transaction in transactions:
            month_key = transaction.date.strftime("%Y-%m")
            monthly_summary[month_key] = monthly_summary.get(month_key, 0.0) + float(transaction.amount)

            category_name = transaction.category.name if transaction.category else "uncategorized"
            category_summary[category_name] = category_summary.get(category_name, 0.0) + float(transaction.amount)

        current_month = datetime.now().strftime("%Y-%m")
        budgets = self.get_budgets(current_month)
        budget_status = []
        for budget in budgets:
            category_total = category_summary.get(budget.category_name, 0.0)
            budget_status.append({
                "category": budget.category_name,
                "limit": round(budget.monthly_limit, 2),
                "spent": round(category_total, 2),
                "remaining": round(budget.monthly_limit - category_total, 2),
                "is_over": category_total > budget.monthly_limit,
            })

        return {
            "transaction_count": len(transactions),
            "total_spending": round(total_spending, 2),
            "monthly_summary": [{"month": month, "total": round(total, 2)} for month, total in sorted(monthly_summary.items())],
            "category_breakdown": [{"category": category, "total": round(total, 2)} for category, total in sorted(category_summary.items())],
            "trend_series": [{"month": month, "total": round(total, 2)} for month, total in sorted(monthly_summary.items())],
            "budget_status": budget_status,
        }

    def set_budget(self, category_name: str, monthly_limit: float, month: str | None = None) -> Budget:
        month_key = month or datetime.now().strftime("%Y-%m")
        budget = self.session.scalar(select(Budget).where(Budget.category_name == category_name, Budget.month == month_key))
        if budget is None:
            budget = Budget(category_name=category_name, monthly_limit=monthly_limit, month=month_key)
            self.session.add(budget)
        else:
            budget.monthly_limit = monthly_limit
        self.session.commit()
        self.session.refresh(budget)
        return budget

    def get_budgets(self, month: str | None = None) -> list[Budget]:
        month_key = month or datetime.now().strftime("%Y-%m")
        return list(self.session.scalars(select(Budget).where(Budget.month == month_key).order_by(Budget.category_name)).all())

    def _get_or_create_category(self, name: str) -> Category:
        category = self.session.scalar(select(Category).where(Category.name == name))
        if category is None:
            category = Category(name=name)
            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)
        return category
