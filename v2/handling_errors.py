import logging
import logging.config
import time
import random
import datetime
from pymongo import MongoClient
from datetime import timezone, timedelta
from py_random_words import RandomWords
from tqdm import tqdm
import maskpass
from pymongo.errors import (
    PyMongoError,
    CollectionInvalid,
    ConfigurationError,
    ConnectionFailure,
    ExecutionTimeout,
)
from connect.connect import ConnectToRpi4
from main import TaskManager

import json


user_name = input("Enter your username: ")  # When use inputs
password = maskpass.askpass(prompt="Enter your password: ", mask="*")
host = "192.168.1.81"  # IP of RPI4
port = 27017
db_name = input("Enter your database name: ")
collection_name = input("Enter name of collection: ")


db = ConnectToRpi4(
    user_name=user_name,
    user_passwd=password,
    host=host,
    port=port,
    db_name=db_name,
    collection_name=collection_name,
)

task = TaskManager(db)
query = {"names": "alpaca"}
update = {"price": 500}
print(task.update_one(query=query, update=update))


def filter_price() -> list:
    try:
        return task.filter_fields({"price": {"$gte": 100}}, {"price": 1})

    except CollectionInvalid as e:
        print("An error occurred --> :", str(e))
        return False

    except PyMongoError as e:
        print("An error occurred --> :", str(e))
        return False


def create_collection():
    try:
        task.create_task({"name": "Giedrius", "job_name": "welder"})
        return True

    except CollectionInvalid as e:
        print("CollectionInvalid --> :", str(e))
        return False

    except PyMongoError as e:
        print("An error occurred --> :", str(e))
        return False


# print(filter_price())
# print(create_collection())


# def connect_with_config_file(config: str) -> MongoClient:
#     """# aptinka kai tik tais pakeičiamas uri = mongodb:// į
#     uri = mongodb:/
#     """
#     try:
#         with open(config, "r") as f:
#             config = json.load(f)

#         host = config.get("host")
#         port = config.get("port")
#         username = config.get("user_name")
#         password = config.get("user_psswd")
#         auth_source = config.get("database")
#         collection_name = config.get("collection")

#         # connection_string = (
#         #     f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
#         # )
#         db = ConnectToRpi4(
#             user_name=username,
#             user_passwd=password,
#             host=host,
#             port=port,
#             db_name=auth_source,
#             collection_name=collection_name,
#         )

#         task = TaskManager(db)

#         return task.filter_fields({"price": {"$gte": 100}}, {"price": 1})

#     except ConfigurationError as e:
#         print("Configuration error:", str(e))
#         return None

#     except PyMongoError as e:
#         print("An error occurred:", str(e))
#         return None


# config_file = "config.json"

# client = connect_with_config_file(config_file)
# print(client)


# def connect_to_mongodb(config: str) -> MongoClient:
#     '''aptinkama klaida kai atjungiamas kabelis nuo RPI'''
#     try:
#         with open(config, "r") as f:
#             config = json.load(f)

#         host = config.get("host")
#         port = config.get("port")
#         username = config.get("user_name")
#         password = config.get("user_psswd")
#         auth_source = config.get("database")
#         collection_name = config.get("collection")

#         # connection_string = (
#         #     f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
#         # )
#         db = ConnectToRpi4(
#             user_name=username,
#             user_passwd=password,
#             host=host,
#             port=port,
#             db_name=auth_source,
#             collection_name=collection_name,
#         )

#         task = TaskManager(db)
#         return task.filter_fields({"price": {"$gte": 100}}, {"price": 1})

#     except ConnectionFailure as e:
#         print("Connection failure:", str(e))
#         return None

#     except PyMongoError as e:
#         print("An error occurred:", str(e))
#         return None


# config_file = "config.json"
# # Usage
# print(connect_to_mongodb(config_file))


# def connect_to_mongodb(config: str, timeout_ms: int) -> list:
#     """Query execution timeout: operation exceeded time limit,
#     full error: {'ok': 0.0, 'errmsg': 'operation exceeded time limit',
#     'code': 50, 'codeName': 'MaxTimeMSExpired'}
#     """
#     try:
#         with open(config, "r") as f:
#             config = json.load(f)

#         host = config.get("host")
#         port = config.get("port")
#         username = config.get("user_name")
#         password = config.get("user_psswd")
#         auth_source = config.get("database")
#         collection_name = config.get("collection")

#         # connection_string = (
#         #     f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
#         # )
#         db = ConnectToRpi4(
#             user_name=username,
#             user_passwd=password,
#             host=host,
#             port=port,
#             db_name=auth_source,
#             collection_name=collection_name,
#         )
#         task = TaskManager(db)
#         query = {"price": {"$gte": 100}}
#         query_options = {"$query": query, "$maxTimeMS": timeout_ms}
#         return task.filter_fields_only_by_query(query_options)
#     except ExecutionTimeout as e:
#         print("Query execution timeout:", str(e))
#         return []

#     except PyMongoError as e:
#         print("An error occurred:", str(e))
#         return []


# config_file = "config.json"
# print(connect_to_mongodb(config=config_file, timeout_ms=1))
