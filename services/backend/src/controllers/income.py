from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

from ..models.user import User
from ..models.income import Income
from ..crud.income import *
from ..auth.security import get_current_active_user

income_router = APIRouter()

@income_router.post("/add_income/", summary="Add income", status_code=status.HTTP_201_CREATED)
async def add_income(request: Request, income: Income, current_user: User = Depends(get_current_active_user)) -> Income:
    income = jsonable_encoder(income)
    createIncome(request.app.database, income)
    return income

@income_router.get("/{income_id}", response_model=Income)
async def get_income(request: Request, income_id: str):
    if (income:= getIncome(request.app.database, income_id)) is not None:
        return income
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Could not find income {income_id}")

@income_router.get("/total/{user_name}", summary="Get total income for a user in a month",response_model=list[dict])
async def get_total_income_user(request: Request, user_name: str, month: int):
    if (total := getUserTotalIncome(request.app.database, user_name, month)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get total income for the user {user_name}")

@income_router.get("/category/{user_name}", summary="Get total income by catgeory for a user in a month", response_model=list[dict])
async def get_total_income_user_category(request: Request, user_name: str, month: int):
    if (total := getUserTotalIncomeByCategory(request.app.database, user_name, month)) is not None:
        return total
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"Could not get total income for the user {user_name}")
