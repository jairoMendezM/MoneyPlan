from fastapi import FastAPI
from pymongo import MongoClient
from Controllers.user_routes import user_router
from profiles.database_connection import DATABASE_NAME, CONNECTION_STRING

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(CONNECTION_STRING)
    app.database = app.mongodb_client[DATABASE_NAME]
    # set_database_collection()
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Stoping Database Connection")

app.include_router(user_router)