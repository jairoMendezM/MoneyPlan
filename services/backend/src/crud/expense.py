import uuid
from typing import Optional, Union
from pymongo import database as Database
from datetime import date as Date
from fastapi import Depends, HTTPException, status

def createExpense(database: Database, expense: dict):
    return database.expense.insert_one(expense)

def getExpense(database: Database, expense_id: Union[str, uuid.UUID]):
    return database.expense.find_one({'_id': expense_id})

def getExpensesByUser(database: Database, user_name: str, from_date: Date, to_date: Date):
    query = {
                "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                "user_name": user_name
            }
    return list(database.expense.find(query))

def getUserExpenseByCategory(database: Database, user_name: str, from_date: Date, to_date: Date, category: Optional[str] = None):
    if category:
        query = [
            {
                '$project': {
                    '_id': 0,
                    'user_name': 1,
                    'bill': 1,
                    'category': 1,
                    'date': 1,
                    'subcategory': 1
                }
            },
            {
                '$match': {
                    "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                    "user_name": user_name
                }
            },
            {'$group': {'_id': '$subcategory', 'total': {'$sum': '$bill'}}}
        ]
        total = list(database.expense.aggregate(query))
    else:
        query = [
            {
                '$project': {
                    '_id': 0,
                    'user_name': 1,
                    'bill': 1,
                    'category': 1,
                    'date': 1,
                }
            },
            {
                '$match': {
                    "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                    "user_name": user_name
                }
            },
            {'$group': {'_id': '$category', 'total': {'$sum': '$bill'}}}
        ]
        total = database.expense.aggregate(query)
    return total

def deleteExpensesByUser(database: Database, user_name: str, id: Optional[ Union[str, uuid.UUID]] = None):
    if id:
        try:
            database.expense.delete_one({'user_name': user_name, '_id': id})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete expense for user {user_name}")
    else:
        try:
            database.expense.delete_many({'user_name': user_name})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete expenses for user {user_name}")