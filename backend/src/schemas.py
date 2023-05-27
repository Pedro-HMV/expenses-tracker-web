from pydantic import BaseModel


class ExpenseBase(BaseModel):
    title: str
    cost: float | None
    due: int | None


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    paid: bool
    owner_id: int
    overdue: bool

    class Config:
        orm_mode = True


class ExpensePartialUpdate(BaseModel):
    title: str | None
    cost: float | None
    due: int | None


class UserBase(BaseModel):
    username: str
    income: float = 0.0


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    net_worth: float
    expenses: list[Expense] = []

    class Config:
        orm_mode = True


class UserPartialUpdate(BaseModel):
    username: str | None
    income: float | None
    income: float | None
    income: float | None
