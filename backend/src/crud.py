from typing import List

from sqlalchemy.orm import Session

from .models import Expense, User
from .schemas import (
    ExpenseCreate,
    ExpensePartialUpdate,
    UserCreate,
    UserPartialUpdate,
)


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        income=user.income,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user_id: int, user: UserPartialUpdate
) -> User | None:
    if db_user := db.query(User).filter(User.id == user_id).first():
        for attr, value in user.dict().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
        return db_user


def get_user_expenses(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Expense]:
    return (
        db.query(Expense)
        .filter(Expense.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_expenses_by_title(
    db: Session, title: str, skip: int = 0, limit: int = 100
) -> List[Expense]:
    return (
        db.query(Expense)
        .filter(
            Expense.title == title,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()


def create_expense(
    db: Session, expense: ExpenseCreate, user_id: int
) -> Expense:
    db_expense = Expense(**expense.dict(), owner_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(
    db: Session, expense_id: int, expense: ExpensePartialUpdate
) -> Expense | None:
    if (
        db_expense := db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    ):
        for attr, value in expense.dict().items():
            if value:
                setattr(db_expense, attr, value)
        db.commit()
        db.refresh(db_expense)
        return db_expense


def toggle_paid_expense(db: Session, expense_id: int) -> Expense | None:
    if (
        db_expense := db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    ):
        db_expense.paid = not db_expense.paid  # type: ignore
        db.commit()
        db.refresh(db_expense)
        return db_expense


def delete_expense(db: Session, expense_id: int) -> None:
    if (
        db_expense := db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    ):
        db.delete(db_expense)
        db.commit()


def delete_user(db: Session, user_id: int) -> None:
    if db_user := db.query(User).filter(User.id == user_id).first():
        db.delete(db_user)
        db.commit()
