import logging
import logging.config
import time
import random
import datetime
from datetime import timezone, timedelta
from py_random_words import RandomWords
from tqdm import tqdm
import maskpass
from names_generator import generate_name
from connect.connect import ConnectToRpi4
from main import TaskManager


user_name = input("Enter your username: ")  # When use inputs

password = maskpass.askpass(prompt="Enter your password: ", mask="*")

host = "192.168.1.81"  # IP of RPI4

port = 27017

db_name = input("Enter your database name: ")

collection_name = input("Enter name of collection: ")


db = ConnectToRpi4(
    user_name=user_name,
    user_passwd=password,
    host=host,
    port=port,
    db_name=db_name,
    collection_name=collection_name,
)

task = TaskManager(db)


def choose_type_of_field() -> int:
    while True:
        try:
            field_type = int(
                input(
                    "Choose type of field:\n1.String(random words)\n2.Integer\n3.Float\n4.UTC\n5.Full name\n6.Only date\n7.Exit\nChoose: "
                )
            )
            return field_type
        except ValueError:
            print("! -- Wrong input, must to be a number -- !", end="\n")
            continue


def min_max_value() -> list:
    while True:
        try:
            min_value, max_value = [
                int(x)
                for x in input("Enter two values (min, max), separated by ',': ").split(
                    ","
                )
            ]
            return min_value, max_value
        except ValueError:
            print("! -- Wrong input, must to be a number -- !", end="\n")
            continue


def create_utc_datetime_min_max(difference_1: int, difference_2: int) -> datetime:
    (dt := datetime.datetime.now(timezone.utc))
    min_difference = dt.year - difference_1
    max_difference = min_difference - difference_2
    rnd_years = random.randint(max_difference, min_difference)
    random_date = datetime.datetime(rnd_years, 1, 12)
    return random_date


def create_utc_datetime(value: int) -> datetime:
    (dt := datetime.datetime.now(timezone.utc))
    new_year = value * 365
    random_years = random.randint(0, new_year)
    rnd_time = random.randint(1, 59)
    new_date = dt - timedelta(
        days=random_years,
        hours=rnd_time,
        minutes=rnd_time,
        seconds=rnd_time,
    )
    return new_date


def not_except_string(string: str) -> int:
    while True:
        try:
            integer = int(input(string))
            return integer
        except ValueError:
            print("! -- Wrong input, must to be a integer -- !", end="\n")
            continue


def input_one_integer():
    while True:
        try:
            i = int(input("How many documents do you want to create? "))
            return i
        except ValueError:
            print("! -- Wrong input, must to be a integer -- !", end="\n")
            continue


dict_of_collection = {}


while True:
    field_name = input("Name of field: ")

    field_type = choose_type_of_field()

    if field_type == 1:
        dict_of_collection.update({field_name: "str"})

    elif field_type == 2:
        value = min_max_value()
        dict_of_collection.update({field_name: ("int", value[0], value[1])})

    elif field_type == 3:
        value = min_max_value()
        value_rounding = not_except_string("Rounding value: ")
        dict_of_collection.update(
            {field_name: ("float", value[0], value[1], value_rounding)}
        )

    elif field_type == 4:
        year_diff = not_except_string("Year difference: ")
        dict_of_collection.update({field_name: ("utc", year_diff)})

    elif field_type == 5:
        dict_of_collection.update({field_name: "fname"})

    elif field_type == 6:
        value = min_max_value()
        dict_of_collection.update({field_name: ("onlydate", value[0], value[1])})

    elif field_type == 7:
        print("*** Field created successfully! ***\n")
        break


i = input_one_integer()


for _ in tqdm(range(0, i), desc="Progress..."):
    document_of_collection = {}
    for keys, values in dict_of_collection.items():
        if values == "str":
            r = RandomWords()
            document_of_collection.update({keys: r.get_word()})

        if values[0] == "int":
            random_value = random.randint(values[1], values[2])
            document_of_collection.update({keys: random_value})

        if values[0] == "float":
            random_value = round(random.uniform(values[1], values[2]), values[3])
            document_of_collection.update({keys: random_value})

        if values[0] == "utc":
            document_of_collection.update({keys: create_utc_datetime(values[1])})

        if values[0] == "fname":
            document_of_collection.update({keys: generate_name(style="capital")})

        if values[0] == "onlydate":
            document_of_collection.update(
                {keys: create_utc_datetime_min_max(values[1], values[2])}
            )

    time.sleep(0.01)
    task.create_task(task=document_of_collection)
print("*** Documents created successfully! ***")
