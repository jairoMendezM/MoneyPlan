# from configparser import ConfigParser
# config = ConfigParser()
# config.read("config_file")
# database_config = config["DATABASE_CONFIG"]
# authentication_config = config["AUTHENTICATION"]
# print(type(authentication_config))

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_name: str
    database_url: str

    client_origin: str

    access_token_expires_in: int
    jwt_algorithm: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file="./config/.env")

settings = Settings()

# https://codevoweb.com/crud-restful-api-server-with-python-fastapi-and-mongodb/
# https://codevoweb.com/api-with-python-fastapi-and-mongodb-jwt-authentication/
# https://fastapi.tiangolo.com/ru/advanced/settings/#__tabbed_2_1