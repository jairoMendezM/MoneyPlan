import uuid
from typing import Optional, Union
from pymongo import database as Database

def createIncome(database: Database, income: dict):
    return database.income.insert_one(income)

def getIncome(database: Database, income_id: Union[str, uuid.UUID]):
    return database.income.find_one({'_id': income_id})

def getUserTotalIncome(database: Database, user_name: str, month: int, category: Optional[str] = None):
    query = [
        {
            '$project': {
            '_id': 0,
            'user_name': 1,
            'income': 1,
            'category': 1,
            'month': {'$month': {'$dateFromString': { 'dateString': '$date', 'format': '%Y-%m-%d' }}},}},
        {'$match': {'month': month, 'user_name': user_name}},
        {'$group': {'_id': '$user_name', 'total': {'$sum': '$income'}}}
    ]
    total = list(database.income.aggregate(query))

    return total

def getUserTotalIncomeByCategory(database: Database, user_name: str, month: int, category: Optional[str] = None):
    if category:
        query = [
            {
                '$project': {
                '_id': 0,
                'user_name': 1,
                'income': 1,
                'category': 1,
                'month': {'$month': {'$dateFromString': { 'dateString': '$date', 'format': '%Y-%m-%d' }}},}},
            {'$match': {'month': month, 'user_name': user_name, 'category': category}},
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
                'month': {'$month': {'$dateFromString': { 'dateString': '$date', 'format': '%Y-%m-%d' }}},}},
            {'$match': {'month': month, 'user_name': user_name}},
            {'$group': {'_id': '$category', 'total': {'$sum': '$income'}}}
        ]
        total = list(database.income.aggregate(query))

    return total