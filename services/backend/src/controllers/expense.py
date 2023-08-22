import uuid
from typing import Optional, Union
from datetime import date as Date

from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

from ..models.user import User
from ..models.expense import Expense
from ..models.auth import Status

from ..crud.expense import (
    getExpense,
    createExpense,
    getExpensesByUser,
    getUserExpenseByCategory,
    deleteExpensesByUser
)
from ..crud.category import (
    getCategory
)

from ..crud.budget import (
    getBudgetByCategory,
    updateBudget
)

from ..auth.security import get_current_active_user

# HELPERS
def in_budget(request, expense, user):
    if (budget := getBudgetByCategory(request.app.database, user['user_name'], expense.category)) is not None:
        if (budget["from_date"] <= expense["date"] <= budget["to_date"]):
            budget['balance'] -= expense.bill
            balance_percentage = 100 * (budget["balance"] / budget["balance"])
            if balance_percentage >= budget["percentage_threshold"]:
                print("THIS IS AN ALERT") # TODO SEND ALERT
            print("updating budget")
            updateBudget(request.app.database, budget)
            
expense_router = APIRouter()

@expense_router.post("/", response_description="Add new expense", status_code=status.HTTP_201_CREATED)
async def add_expense(request: Request, expense: Expense, current_user: User = Depends(get_current_active_user)) -> Expense:
    if (category := getCategory(request.app.database, expense.category)) is not None:
        if expense.subcategory in category["subcategories"] and category["type"]:
            if expense.bill > 0:
                # Check if it exists a budget related to expense category TODO
                expense = jsonable_encoder(expense)
                createExpense(request.app.database, expense)
                return expense
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Bill should be greater than 0.")
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Subcategory {expense.subcategory} does not exist for category {expense.category}")
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Category {expense.category} does not exist")

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

@expense_router.delete("/")
async def delete_expense_by_user(request: Request, id: Optional[Union[str, uuid.UUID]] = None,
                                current_user: User = Depends(get_current_active_user)):
    result = deleteExpensesByUser(request.app.database, current_user["user_name"], id)
    if result == status.HTTP_200_OK:
        return Status(message=f"Expense deleted")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete expense for user {current_user['user_name']}")