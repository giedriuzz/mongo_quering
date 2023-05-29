from pymongo import MongoClient
from dataclasses import dataclass
from pymongo.database import Database


class Connect:  # Leaved if use a docker on compatible machine without user authentication
    def connect_to_mongodb(self, host: str, port: int, db_name: str) -> Database:
        client = MongoClient(host, port)
        database = client[db_name]
        return database


@dataclass
class ConnectToRpi4:
    user_name: str
    user_passwd: str
    host: str
    port: int
    db_name: int
    collection_name: str


if __name__ == "__main__":
    pass
