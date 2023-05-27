from datetime import datetime

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    income = Column(Float, nullable=True)

    expenses = relationship("Expense", back_populates="owner")

    @property
    def net_worth(self) -> float:
        return self.income - sum(expense.cost for expense in self.expenses)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    cost = Column(Float, nullable=True)
    due = Column(Integer, nullable=True)
    paid = Column(Boolean, default=False)

    owner = relationship("User", back_populates="expenses")
    owner_id = Column(Integer, ForeignKey("users.id"))

    @property
    def overdue(self) -> bool:
        return (
            self.due is not None
            and not self.paid
            and datetime.now().day > self.due
        )
