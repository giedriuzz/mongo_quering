from pymongo import MongoClient
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

    def update_one(self, query: Dict, update: Dict[str, Any]) -> int:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return list(self.collection.find())

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

    def filter_by_greater_than_equal(self, field_name: str, value: int) -> List[dict]:
        """$gte	It will match all the values that are greater than or equal to a specified value."""
        query = {field_name: {"$gte": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_less_than_equal(self, field_name: str, value: int) -> List[dict]:
        """$lte	It will match all the values that are less than or equal to a specified value."""
        query = {field_name: {"$lte": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_in(self, field_name: str, value: List[int]) -> List[dict]:
        query = {field_name: {"$in": value}}
        result = self.collection.find(query)
        return list(result)

    def filter_by_not_in(self, field_name: str, value: List[int]) -> List[dict]:
        query = {field_name: {"$nin": value}}
        result = self.collection.find(query)
        return list(result)

    """all items (name and year made) where the quantity is less or equal to 10 and the price is equal or less of 20.00."""

    def filter_by_less_than_equal_two_fields(
        self,
        first_field: str,
        first_value: int,
        second_field: str,
        second_value: int,
        sort_fields,
    ) -> List[dict]:
        """$lte	It will match all the values that are less than or equal to a specified value."""
        query = {
            first_field: {"$lte": first_value},
            "$and": [{second_field: {"$lte": second_value}}],
        }
        fields = {**sort_fields}
        result = self.collection.find(query, fields)
        return list(result)

    def filter_by_greater_than_equal_two_fields(
        self, first_field: str, first_value: int, second_field: str, second_value: int
    ) -> List[dict]:
        """$lte	It will match all the values that are less than or equal to a specified value."""
        query = {
            first_field: {"$gte": first_value},
            "$and": [{second_field: {"$gte": second_value}}],
        }

        result = self.collection.find(query)
        return list(result)

    def filter_fields(self, collection: str, keys_values) -> List[dict]:
        query = {**keys_values}
        collections = {**collection}
        result = self.collection.find(collections, query)
        return list(result)

    def filter_fields_only_by_query(self, collection: str) -> List[dict]:
        collections = {**collection}
        result = self.collection.find(collections)
        return list(result)


if __name__ == "__main__":
    pass
