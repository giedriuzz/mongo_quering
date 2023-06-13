import logging
import logging.config
import time
import random
import datetime
from typing import Union
from pymongo import MongoClient
from datetime import timezone, timedelta
from py_random_words import RandomWords
from tqdm import tqdm
import maskpass
from pymongo.errors import (
    PyMongoError,
    CollectionInvalid,
    NetworkTimeout,
    AutoReconnect,
    WriteError,
)
from connect.connect import ConnectToRpi4
from main import TaskManager

import json


def connect_to_db_with_config(config: str):
    with open(config, "r") as f:
        config = json.load(f)

        host = config.get("host")
        port = config.get("port")
        username = config.get("user_name")
        password = config.get("user_psswd")
        auth_source = config.get("database")

        db = ConnectToRpi4(
            user_name=username,
            user_passwd=password,
            host=host,
            port=port,
            db_name=auth_source,
        )

    return db


config_file = "config.json"
connection = connect_to_db_with_config(config=config_file)
querying = TaskManager(collection="pets", base=connection)


def filter_price() -> Union[list, bool]:
    print("****************************************************************")
    try:
        return querying.filter_fields({"price": {"$gte": 999}}, {"price": 1})

    except CollectionInvalid as e:
        print("CollectionInvalid an error occurred --> :", str(e))
        return False
    except NetworkTimeout as e:
        print("NetworkTimeout an error occurred --> :", str(e))
        return False
    except AutoReconnect as e:
        """Rise AutoReconnect when:
        1) bad IP address
        2) bad port number
        3) unconnected LAN  cable
        """
        print("AutoReconnect an error occurred --> :", str(e))
        return False
    except PyMongoError as e:
        """Rise PyMongoError when:
        1) bad db user name
        2) bad db user password"""
        print("PyMongoError an error occurred --> :", str(e))
        return False


if filter_price():
    print(filter_price())
else:
    i = 0
    while i < 3:
        if filter_price():
            print(filter_price())
        else:
            i += 1
            print(f"{i} attempts")


# def create_collection() -> bool:
#     try:
#         querying.create_task(
#             {
#                 "name": "cow",
#                 "price": 100,
#                 "quantity": 23,
#                 "birth_day": "2022-04-02T12:17:40.201Z",
#             }
#         )
#         return True

#     except CollectionInvalid as e:
#         print("CollectionInvalid --> :", str(e))
#         return False
#     except WriteError as e:
#         print("WriteError --> :", str(e))
#         return False
#     except PyMongoError as e:
#         print("An error occurred --> :", str(e))
#         return False


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
#         #     f"mongodb:///{username}:{password}@{host}:{port}/{auth_source}"
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
