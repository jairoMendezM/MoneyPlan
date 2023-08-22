from .controllers.user import user_router
from .controllers.income import income_router
from .controllers.expense import expense_router
from .controllers.category import category_router
from .controllers.budget import budget_router

from .db.register import database_connection

from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

database_connection(app)

app.include_router(user_router, tags=['Auth'], prefix='/user')
app.include_router(income_router, tags=['User/Income'], prefix='/user/income')
app.include_router(expense_router, tags=['User/Expense'], prefix='/user/expense')
app.include_router(category_router, tags=['Category'], prefix="/category")
app.include_router(budget_router, tags=['Budget'], prefix="/budget")

# python -m uvicorn main:app --reload