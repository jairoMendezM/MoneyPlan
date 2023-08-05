from ..models.expense import Expense
from ..crud.expense import *

from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

expense_router = APIRouter()

@expense_router.post("/user/expense/add_expense/", response_description="Add expense", status_code=status.HTTP_201_CREATED)
async def add_expense(request: Request, expense: Expense) -> Expense:
    expense = jsonable_encoder(expense)
    createExpense(request.app.database, expense)
    return expense

@expense_router.get("/user/expense/{expense_id}", response_model=Expense)
async def get_expense(request: Request, expense_id: str):
    if (expense:= getExpense(request.app.database, expense_id)) is not None:
        return expense
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find expense {expense_id}")

@expense_router.get("/user/expense/total/{user_name}", response_model=list[dict])
async def get_user_total_expense(request: Request, user_name: str, month: int, category: Optional[str] =None):
    if (total := getUserExpenseByCategory(request.app.database, user_name, month, category)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get expense total for the user {user_name}")