from pymongo import MongoClient
from pymongo.database import Database
import maskpass
from dataclasses import dataclass


class Connect:
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


# Example usage
if __name__ == "__main__":
    pass
