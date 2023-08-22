import uuid
from typing import Union, Optional
from datetime import date as Date

from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Body, Depends
from fastapi.encoders import jsonable_encoder

from ..models.user import User
from ..models.budget import Budget
from ..models.auth import Status

from ..crud.budget import (
    createBudget,
    deleteBudgetsByUser,
    getBudgetsByUser,
    getBudgetByUserByCategory
)

from ..auth.security import get_current_active_user

budget_router = APIRouter()

@budget_router.post("/create", summary="Create new budget", response_model=Budget)
async def create_budget(request: Request, budget: Budget, current_user: User = Depends(get_current_active_user)):
    budget = jsonable_encoder(budget)
    createBudget(request.app.database, budget)
    return budget

@budget_router.get("/{from_date}-{to_date}", summary="Get budgets by user", response_model=list)
async def get_user_budgets(request: Request, from_date: Date, to_date: Date,
                           current_user: User = Depends(get_current_active_user)):
    return getBudgetsByUser(request.app.database, current_user['user_name'], from_date, to_date)

@budget_router.get("/{category}/{from_date}-{to_date}", summary="Get budgets by user and category", response_model=list)
async def get_user_budgets_category(request: Request, from_date: Date, to_date: Date, category: str,
                                    current_user: User = Depends(get_current_active_user)):
    return getBudgetByUserByCategory(request.app.database, current_user['user_name'], from_date, to_date, category)

@budget_router.delete("/", summary="Delete budget")
async def delete_budget(request: Request, id: Optional[Union[str, uuid.UUID]] = None, current_user: User = Depends(get_current_active_user)):
    result = deleteBudgetsByUser(request.app.database, current_user['user_name'], id)
    if result == status.HTTP_200_OK:
        return Status(message=f"Budget deleted")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete expense for user {current_user['user_name']}")