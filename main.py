from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Any, Optional


class TaskManager:
    def __init__(
        self,
        host: str,
        user_name: str,
        user_passwd: str,
        port: int,
        db_name: str,
        collection_name: str,
    ) -> None:
        uri = "mongodb://ufo:pempiai234@192.168.1.81:27017"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_task(self, task: Dict[str, Any]) -> str:
        result = self.collection.insert_one(task)
        return str(result.inserted_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return list(self.collection.find())

    # def get_task(self, task_name: str) -> Dict[str, Any]:
    #     return list(self.collection.find({​"task_name": task_name}​))

    # def update_task(self, task_name: str, task_updates: Dict[str, Any]) -> bool:
    #     result = self.collection.update_one(
    #         {​"task_name": task_name}​, {​"$set": task_updates}​
    #     )
    #     return result.modified_count > 0

    # def delete_task(self, task_name: str) -> bool:
    #     result = self.collection.delete_one({​"task_name": task_name}​)
    #     return result.deleted_count > 0

    def filter_by_equals(self, field_name: str, value: str) -> List[dict]:
        """$eq It will match the values that are equal to a specified value."""
        query = {field_name: {"$eq": value}}
        result = self.collection.find_one(query)
        return list(result)

    def filter_by_not_equals(self, field_name: str, value: str) -> List[dict]:
        """$ne It will match all the values that are not equal to a specified value."""
        query = {field_name: {"$ne": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_greater_than(self, field_name: str, value: int) -> List[dict]:
        """$qt It will match the values that are greater than a specified value."""
        query = {field_name: {"$gt": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_less_than(self, field_name: str, value: int) -> List[dict]:
        """$lt It will match all the values that are less than a specified value."""
        query = {field_name: {"$lt": value}}
        result = self.collection.find(query)
        return list(result)

    def get_single_query(
        self, query: Dict[str, Any], fields: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query, fields)


if __name__ == "__main__":
    db = TaskManager(
        host="localhost",
        user_name="aa",
        user_passwd="ddd",
        port=27017,
        db_name="cafeteria",
        collection_name="new",
    )

    # print(db.filter_by_equals("value", 115), "\n")
    lists = db.filter_by_not_equals("value", 20)
    for n in lists:
        print(n)

    print(db.get_all_tasks())
