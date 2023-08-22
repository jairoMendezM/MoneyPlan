from fastapi import APIRouter, Request, HTTPException, status
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from datetime import date as Date
from typing import Optional, Union

from ..models.user import User
from ..models.category import Category
from ..models.auth import Status

from ..crud.category import *

from ..auth.security import get_current_active_user

category_router = APIRouter()

@category_router.post("/create", response_model=Category)
async def create_category(request: Request, category: Category, current_user: User = Depends(get_current_active_user)):
    category = jsonable_encoder(category)
    createCategory(request.app.database, category)
    return category

@category_router.get("/{category}", response_model=Category)
async def get_category(request: Request, category: str, current_user: User = Depends(get_current_active_user)):
    return getCategory(request.app.database, category)

@category_router.get("/subcategories/{category}", response_model=dict)
async def get_subcategory(request: Request, category: str, current_user: User = Depends(get_current_active_user)):
    return getSubCategories(request.app.database, category)

@category_router.get("/", summary="Get all categories")
async def get_categories(request: Request, current_user: User = Depends(get_current_active_user)):
    return getAllCategories(request.app.database)

@category_router.put("/{category}/{add}_{subcategory}")
async def update_category(request: Request, category: str, add: bool, subcategory: str,
                          current_user: User = Depends(get_current_active_user)):
    if add:
        return addSubCategory(request.app.database, category, subcategory)
    else:
        return deleteSubCategory(request.app.database, category, subcategory)

@category_router.delete("/{category}")
async def delete_category(request: Request, category: str, current_user: User = Depends(get_current_active_user)):
    return deleteCategory(request.app.database, category)