from typing import Optional
from datetime import date as Date

from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

from ..models.user import User
from ..models.expense import Expense
from ..models.auth import Status

from ..crud.expense import *

from ..auth.security import get_current_active_user

expense_router = APIRouter()

@expense_router.post("/add_expense/", response_description="Add new expense", status_code=status.HTTP_201_CREATED)
async def add_expense(request: Request, expense: Expense, current_user: User = Depends(get_current_active_user)) -> Expense:
    expense = jsonable_encoder(expense)
    createExpense(request.app.database, expense)
    return expense

@expense_router.get("/{expense_id}", summary="Get an specific expense", response_model=Expense)
async def get_expense(request: Request, expense_id: str, current_user: User = Depends(get_current_active_user)):
    if (expense:= getExpense(request.app.database, expense_id)) is not None:
        return expense
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find expense {expense_id}")

@expense_router.get("/all/", summary="Get user expenses by a period of time")
async def get_user_expenses(request: Request, from_date: Date, to_date: Date,
                            current_user: User = Depends(get_current_active_user)):
    if(expenses := getExpensesByUser(request.app.database,current_user['user_name'], from_date, to_date)) is not None:
        return expenses
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find expenses for user {current_user['user_name']}")

@expense_router.get("/total/", summary="Get total expense by a period of time for current user. It could be filter by category-subcategory or in total by category",
                    response_model=list[dict])
async def get_user_total_expense(request: Request, from_date: Date, to_date: Date,
                                 category: Optional[str] =None, current_user: User = Depends(get_current_active_user)):
    if (total := getUserExpenseByCategory(request.app.database, current_user['user_name'], from_date, to_date, category)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get expense total for the user {current_user['user_name']}")

@expense_router.delete("/delete")
async def delete_income_by_user(request: Request, user_name: str, id: Optional[Union[str, uuid.UUID]] = None):
    result = deleteExpensesByUser(request.app.database, user_name, id)
    if result == status.HTTP_200_OK:
        return Status(message=f"Expense deleted")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete income for user {user_name}")