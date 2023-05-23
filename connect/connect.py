from pymongo import MongoClient
from pymongo.database import Database


class Connect:
    def connect_to_mongodb(self, host: str, port: int, db_name: str) -> Database:
        client = MongoClient(host, port)
        database = client[db_name]
        return database


# Example usage
if __name__ == "__main__":
    pass
