import uuid
from typing import Union, Optional
from pymongo import database as Database
from datetime import date as Date
from fastapi import Depends, HTTPException, status

def createBudget(database: Database, budget: dict):
    return database.budget.insert_one(budget)

def getBudget(database: Database, budget_id: Union[str, uuid.UUID]):
    return database.budget.find_one({'_id': budget_id})

def getBudgetByCategory(database: Database, user_name: str, category: str, date: Date):
    if (budget := database.budget.find_one({'user_name': user_name, 'category': category})):
        return budget

def getBudgetsByUser(database: Database, user_name: str, from_date: Date, to_date: Date):
    query = {
                "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                "user_name": user_name
            }
    return list(database.budget.find(query, {'_id', 0}))

def getBudgetByUserByCategory(database: Database, user_name: str, category: str, from_date: Date, to_date: Date):
    query = {
                "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                "user_name": user_name,
                'category': category
            }
    return list(database.budget.find(query, {'_id', 0}))

def updateBudget(database: Database, new_budget):
    return database.budget.find_one_and_replace({"_id": new_budget['_id']}, new_budget)

def deleteBudgetsByUser(database: Database, user_name: str, id: Optional[Union[str, uuid.UUID]] = None):
    if id:
        try:
            database.budget.delete_one({'user_name': user_name, '_id': id})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete budget for user {user_name}")
    else:
        try:
            database.budget.delete_many({'user_name': user_name})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete budgets for user {user_name}")