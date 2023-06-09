import datetime
from main import TaskManager
import maskpass
from connect.connect import ConnectToRpi4

# user_name = input("Enter your username: ")
# password = maskpass.askpass(prompt="Enter your password: ", mask="*")
user_name = "ufo"
password = "pempiai234"
host = "192.168.1.81"  # ip of RPI4
port = 27017
# db_name = input("Enter name of database: ")
# collection_name = input("Enter name of collection: ")
db_name = "pets"
collection_name = "pets"

db = ConnectToRpi4(
    user_name=user_name,
    user_passwd=password,
    host=host,
    port=port,
    db_name=db_name,
    collection_name=collection_name,
)

task = TaskManager(db)

# # Monetary
# date = datetime.datetime(2022, 7, 12)
# collections = task.filter_by_less_than(field_name="birth_day", value=date)
# monetary = []
# for collection in collections:
#     monetary.append(collection.get("price"))
# print("Monetary: ", round(sum(monetary), 2), "€")

# # Average price of items
# average_price = []
# items = task.get_all_tasks()
# for i in items:
#     average_price.append(i.get("price"))
# print(
#     "Average sum of items prices: ", round(sum(average_price) / len(average_price), 2)
# )

# # letter a and cots is between 10 and 100
# by_letter = task.filter_by_first_letter_and_two_values(
#     first_field_name="name",
#     letter="a",
#     second_field_name="price",
#     min_price=10,
#     max_price=100,
# )
# print("*** By first letter ***")
# for i in enumerate(by_letter, start=1):
#     print(i, end="\n")

# # letter a and cots is between 10 and 100
# all = task.filter_all_by_two_fields_and_more_and_less_values(
#     first_field_name="price", bigger_then=50, second_field_name="quantity", less_then=10
# )
# print("*** All ***")
# for i in enumerate(all, start=1):
#     for a in i:
#         print(a)

filter_lte = task.filter_by_less_than_equal_two_fields(
    first_field="quantity",
    first_value=100,
    second_field="price",
    second_value=200.00,
    pushed_fields={"name": 1, "birth_day": 1},
)
print(filter_lte)


# by_fields = task.filter_fields(
#     {"quantity": {"$lte": 100}, "$and": [{"price": {"$lte": 200.00}}]},
#     {"name": 1, "birth_day": 1},
# )
# print(by_fields)

# filter_gte = task.filter_by_greater_than_equal_two_fields(
#     first_field="quantity", first_value=100, second_field="price", second_value=200.00
# )
# print(filter_gte)
