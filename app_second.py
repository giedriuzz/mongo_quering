from pymongo import MongoClient
import maskpass
from typing import List, Dict, Optional, Union
from connect.connect import ConnectToRpi4


# user_name = input("Enter your username: ")
# password = maskpass.askpass(prompt="Enter your password: ", mask="*")
user_name = "ufo"
password = "pempiai234"
host = "192.168.1.81"  # ip of RPI4
port = 27017
# db_name = input("Enter name of database: ")
# collection_name = input("Enter name of collection: ")
db_name = "animals"
collection_name = "dogs"


db = ConnectToRpi4(
    user_name=user_name,
    user_passwd=password,
    host=host,
    port=port,
    db_name=db_name,
    collection_name=collection_name,
)


class QueryingPartTwo:
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

    def filter_fields(self, keys_values) -> List[dict]:
        query = {**keys_values}
        result = self.collection.find_one({}, query)
        return list(result)


querying = QueryingPartTwo(db)

equals_or_more = querying.filter_by_greater_than_equal(
    field_name="weight", value=999.19
)
print("Equal or more ------>", equals_or_more, end="\n")

equals_or_less = querying.filter_by_less_than_equal(field_name="quantity", value=1)
print("Less or more ------>", equals_or_less, end="\n")

categories_in = ["bass", "stork"]
filter_by_in = querying.filter_by_in(field_name="name", value=categories_in)
print("Filter by in ------>", filter_by_in, end="\n")

categories_in = ["bass", "stork"]
filter_by_in = querying.filter_by_not_in(field_name="name", value=categories_in)
print("Filter by not in------>", filter_by_in, end="\n")

filter_by = querying.filter_fields({"name": 1, "weight": 1, "born_date": 1})
print(filter_by)
