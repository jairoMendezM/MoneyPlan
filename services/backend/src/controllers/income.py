from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from datetime import date as Date
from typing import Optional, Union
import uuid

from ..models.user import User
from ..models.income import Income
from ..models.auth import Status

from ..crud.income import (
    createIncome,
    getIncome,
    getIncomesByUser,
    getUserTotalIncome,
    getUserTotalIncomeByCategory,
    deleteIncomesByUser
)

from ..auth.security import get_current_active_user

income_router = APIRouter()

@income_router.post("/", summary="Add income", status_code=status.HTTP_201_CREATED)
async def add_income(request: Request, income: Income, current_user: User = Depends(get_current_active_user)) -> Income:
    income = jsonable_encoder(income)
    createIncome(request.app.database, income)
    return income

@income_router.get("/{income_id}", response_model=Income)
async def get_income(request: Request, income_id: str, current_user: User = Depends(get_current_active_user)):
    if (income:= getIncome(request.app.database, income_id)) is not None:
        return income
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find income {income_id}")

@income_router.get("/all/", summary="Get user expenses by a period of time")
async def get_user_expenses(request: Request, from_date: Date, to_date: Date,
                            current_user: User = Depends(get_current_active_user)):
    if(expenses := getIncomesByUser(request.app.database,current_user['user_name'], from_date, to_date)) is not None:
        return expenses
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find incomes for user {current_user['user_name']}")

@income_router.get("/total/", summary="Get total income for a user in a month")
async def get_total_income_user(request: Request, from_date: Date, to_date: Date, current_user: User = Depends(get_current_active_user)):
    if (total := getUserTotalIncome(request.app.database, current_user['user_name'], from_date, to_date)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get total income for the user {current_user['user_name']}")

@income_router.get("/total/category", summary="Get total income by catgeory for a user in a month")
async def get_total_income_user_category(request: Request, from_date: Date, to_date: Date, current_user: User = Depends(get_current_active_user)):
    if (total := getUserTotalIncomeByCategory(request.app.database, current_user['user_name'], from_date, to_date)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get total income for the user {current_user['user_name']}")

@income_router.delete("/")
async def delete_income_by_user(request: Request, user_name: str, id: Optional[Union[str, uuid.UUID]] = None):
    result = deleteIncomesByUser(request.app.database, user_name, id)
    if result == status.HTTP_200_OK:
        return Status(message=f"Income deleted")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete income for user {user_name}")
