import uuid
from typing import Optional, Union
from pymongo import database as Database

def createExpense(database: Database, expense: dict):
    return database.expense.insert_one(expense)

def getExpense(database: Database, expense_id: Union[str, uuid.UUID]):
    return database.expense.find_one({'_id': expense_id})

def getUserExpenseByCategory(database: Database, user_name: str, month: int, category: Optional[str] = None):
    if category:
        query = [
            {
                '$project': {
                '_id': 0,
                'user_name': 1,
                'bill': 1,
                'category': 1,
                'month': {'$month': {'$dateFromString': { 'dateString': '$date', 'format': '%Y-%m-%d' }}},}},
            {'$match': {'month': month, 'user_name': user_name, 'category': category}},
            {'$group': {'_id': '$category', 'total': {'$sum': '$bill'}}}
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
                'month': {'$month': {'$dateFromString': { 'dateString': '$date', 'format': '%Y-%m-%d' }}},}},
            {'$match': {'month': month, 'user_name': user_name}},
            {'$group': {'_id': '$category', 'total': {'$sum': '$bill'}}}
        ]
        total = list(database.expense.aggregate(query))

    return total