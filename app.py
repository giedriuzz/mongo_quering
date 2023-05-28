from main import TaskManager
from py_random_words import RandomWords
import random
from tqdm import tqdm
import time
import maskpass
from datetime import timezone, timedelta
import datetime

# host = "localhost"
host = "192.168.1.81"  # for RPI4
user_name = input("Enter your username: ")
password = maskpass.askpass(prompt="Enter your password: ", mask="*")
port = 27017
db_name = input("Enter name of database: ")
collection_name = input("Enter name of collection: ")


db = TaskManager(
    host=host,
    port=port,
    user_name=user_name,
    user_passwd=password,
    db_name=db_name,
    collection_name=collection_name,
)
dt = datetime.datetime.now(timezone.utc)
dictionary = {}

while True:
    field_name = input("Name of field: ")
    field_type = int(
        input("Choose type of field:\n1.String\n2.Integer\n3.Float\n4.UTC\n5.Exit\n")
    )
    if field_type == 1:
        dictionary.update({field_name: "str"})

    elif field_type == 2:
        min_value = int(input("Enter minimum value: "))
        max_value = int(input("Enter maximum value: "))
        dictionary.update({field_name: ("int", min_value, max_value)})
    elif field_type == 3:
        min_value = int(input("Enter minimum value: "))
        max_value = int(input("Enter maximum value: "))
        value_rounding = int(input("Enter value of rounding: "))
        dictionary.update({field_name: ("float", min_value, max_value, value_rounding)})
    elif field_type == 4:
        year_diff = int(input("Enter year difference: "))
        dictionary.update({field_name: ("utc", year_diff)})
    elif field_type == 5:
        print("*** Field created successfully! ***\n")
        break

i = int(input("How many documents do you want to create? "))


for _ in tqdm(range(0, i), desc="Progress..."):
    document = {}
    for keys, values in dictionary.items():
        if values == "str":
            r = RandomWords()
            document.update({keys: r.get_word()})
        if values[0] == "int":
            random_value = random.randint(values[1], values[2])
            document.update({keys: random_value})
        if values[0] == "float":
            random_value = round(random.uniform(values[1], values[2]), values[3])
            document.update({keys: random_value})
        if values[0] == "utc":
            new_year = values[1] * 365
            random_years = random.randint(0, new_year)
            random_hours = random.randint(1, 59)
            random_minutes = random.randint(1, 59)
            random_seconds = random.randint(1, 59)
            new_date = dt - timedelta(
                days=random_years,
                hours=random_hours,
                minutes=random_minutes,
                seconds=random_seconds,
            )
            only_date = new_date.strftime("%Y-%m-%d")
            document.update({keys: only_date})
    time.sleep(0.01)
    db.create_task(task=document)
print("*** Documents created successfully! ***")
