from typing import Any, Generator, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal

app: FastAPI = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
def get_db() -> Generator[Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> models.User:
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def list_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.User]:
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> models.User:
    db_user: models.User | None = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/expenses/", response_model=schemas.Expense)
def create_expense(
    user_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
) -> models.Expense:
    if expense.due is not None and (expense.due < 1 or expense.due > 31):
        raise HTTPException(
            status_code=400, detail="Day of month must be between 1 and 31"
        )
    expense = crud.create_expense(db=db, expense=expense, user_id=user_id)
    return expense


@app.patch("/users/{user_id}/", response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserPartialUpdate,
    db: Session = Depends(get_db),
) -> models.User | None:
    return crud.update_user(db=db, user_id=user_id, user=user)


@app.patch("/expenses/{expense_id}/payment/", response_model=schemas.Expense)
def toggle_expense_payment(
    expense_id: int, db: Session = Depends(get_db)
) -> models.Expense:
    return crud.toggle_paid_expense(db=db, expense_id=expense_id)


@app.get("/users/{user_id}/expenses/", response_model=List[schemas.Expense])
def list_user_expenses(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[models.Expense]:
    return crud.get_user_expenses(db, user_id=user_id, skip=skip, limit=limit)


@app.delete("/expenses/{expense_id}/")
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> None:
    crud.delete_expense(db=db, expense_id=expense_id)


@app.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    crud.delete_user(db=db, user_id=user_id)


@app.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(
    search: str | int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[models.Expense]:
    if isinstance(search, str):
        return crud.get_expenses_by_title(
            db, title=search, skip=skip, limit=limit
        )
    return crud.get_expense(db, expense_id=search)


@app.patch("/expenses/{expense_id}/", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpensePartialUpdate,
    db: Session = Depends(get_db),
) -> models.Expense | None:
    return crud.update_expense(db=db, expense_id=expense_id, expense=expense)
