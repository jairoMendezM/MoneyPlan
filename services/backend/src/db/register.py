from pymongo import MongoClient

from ..utils.config import settings

def database_connection(app):
    @app.on_event('startup')
    def startup_db_client():
        app.mongodb_client = MongoClient(settings.database_url, serverSelectionTimeoutMS=5000)
        try:
            conn = app.mongodb_client.server_info()
            print(f"Connected to MongoDB {conn.get('version')}")
        except Exception as e:
            print(f'Unable to connect to the MongoDB server. Error {e}')

        app.database = app.mongodb_client[settings.database_name]

    @app.on_event('shutdown')
    def shutdown_db_client():
        app.mongodb_client.close()
        print('Stoping Database Connection')