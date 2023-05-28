from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Any, Optional, Union
from connect.connect import ConnectToRpi4


class TaskManager:
    def __init__(
        self,
        base: ConnectToRpi4,
    ) -> None:
        uri = "mongodb://%s:%s@%s:%s/" % (
            base.user_name,
            base.user_passwd,
            base.host,
            base.port,
        )
        self.db_name = base.db_name
        self.client = MongoClient(uri)
        self.db = self.client[base.db_name]
        self.collection = self.db[base.collection_name]

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

    def filter_by_greater_than(self, field_name: str, value: Any) -> List[dict]:
        """$qt It will match the values that are greater than a specified value."""
        query = {field_name: {"$gt": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_less_than(self, field_name: str, value: int) -> List[dict]:
        """$lt It will match all the values that are less than a specified value."""
        query = {field_name: {"$lt": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_greater_than_or_equals(
        self, field_name: str, value: int
    ) -> List[dict]:
        """$gte It will match the values that are greater than or equal to a specified value."""
        query = {field_name: {"$gte": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_match_any(
        self, field_name: str, value: Union[str, int]
    ) -> Optional[Dict[str, Any]]:
        """'$in It will match any of the values specified in an array."""
        query = {field_name: {"$in": value}}
        result = self.collection.find(query)
        return list(result)

    def get_single_query(
        self, query: Dict[str, Any], fields: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query, fields)

    def filter_by_first_letter_and_two_values(
        self,
        first_field_name: str,
        letter: str,
        second_field_name: str,
        min_price: float,
        max_price: float,
    ) -> List[dict]:
        query = {
            first_field_name: {"$regex": "^" + letter, "$options": "i"},
            "$and": [{second_field_name: {"$gt": min_price, "$lt": max_price}}],
        }
        result = self.collection.find(query)
        return list(result)

    def filter_all_by_two_fields_and_more_and_less_values(
        self,
        first_field_name: str,
        bigger_then: float,
        second_field_name: str,
        less_then: float,
    ) -> List[dict]:
        query = {
            "$and": [
                {first_field_name: {"$gt": bigger_then}},
                {second_field_name: {"$lt": less_then}},
            ]
        }
        result = self.collection.find(query)
        return list(result)


if __name__ == "__main__":
    db = TaskManager(
        host="192.168.1.81",
        user_name="",
        user_passwd="",
        port=27017,
        db_name="pets",
        collection_name="pets",
    )

    # print(db.filter_by_equals("value", 115), "\n")
    lists = db.filter_by_not_equals("value", 20)
    for n in enumerate(lists, start=1):
        print(n, end="\n")

    # print(db.get_all_tasks())

    filtered = db.filter_by_greater_than_or_equals(
        field_name="birth_day", value="2022-05-12"
    )
    print(filtered, end="\n")
