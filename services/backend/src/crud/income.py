import uuid
from typing import Optional, Union
from pymongo import database as Database
from datetime import date as Date
from fastapi import Depends, HTTPException, status

def createIncome(database: Database, income: dict):
    return database.income.insert_one(income)

def getIncome(database: Database, income_id: Union[str, uuid.UUID]):
    return database.income.find_one({'_id': income_id})

def getIncomesByUser(database: Database, user_name: str, from_date: Date, to_date: Date):
    query = {
                "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                "user_name": user_name
            }
    return list(database.income.find(query))

def getUserTotalIncome(database: Database, user_name: str, from_date: Date, to_date: Date, category: Optional[str] = None):
    query = [
        {
            '$project': {
                '_id': 0,
                'user_name': 1,
                'income': 1,
                'category': 1,
                'date': 1
            }
        },
        {
            '$match': {
                "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                "user_name": user_name
            }
        },
        {'$group': {'_id': '$user_name', 'total': {'$sum': '$income'}}}
    ]
    total = list(database.income.aggregate(query))

    return total

def getUserTotalIncomeByCategory(database: Database, user_name: str, from_date: Date, to_date: Date, category: Optional[str] = None):
    if category:
        query = [
            {
                '$project': {
                    '_id': 0,
                    'user_name': 1,
                    'income': 1,
                    'category': 1,
                    'date':1
                 }
            },
            {
                '$match': {
                    "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                    "user_name": user_name
                }
            },
            {'$group': {'_id': '$category', 'total': {'$sum': '$income'}}}
        ]
        total = list(database.income.aggregate(query))
    else:
        query = [
            {
                '$project': {
                    '_id': 0,
                    'user_name': 1,
                    'income': 1,
                    'category': 1,
                    'date': 1
                }
            },
            {
                '$match': {
                    "date": {'$gte': from_date.strftime('%Y-%m-%d'), '$lte': to_date.strftime('%Y-%m-%d')},
                    "user_name": user_name
                }
            },
            {'$group': {'_id': '$category', 'total': {'$sum': '$income'}}}
        ]
        total = list(database.income.aggregate(query))

    return total

def deleteIncomesByUser(database: Database, user_name: str, id: Optional[Union[str, uuid.UUID]] = None):
    if id:
        try:
            database.income.delete_one({'user_name': user_name, '_id': id})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete income for user {user_name}")
    else:
        try:
            database.income.delete_many({'user_name': user_name})
            return status.HTTP_200_OK
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not delete incomes for user {user_name}")