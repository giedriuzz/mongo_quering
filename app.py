import logging
import logging.config
import time
import random
import datetime
from datetime import timezone, timedelta
from py_random_words import RandomWords
from tqdm import tqdm
import maskpass
from connect.connect import ConnectToRpi4
from main import TaskManager

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("sLogger")

logger.debug(" .. Starting logging user and database credentials ..")
user_name = input("Enter your username: ")  # When use inputs
logger.debug(f"User name: {user_name}")
password = maskpass.askpass(prompt="Enter your password: ", mask="*")
logger.debug(f"Password: ************")
host = "192.168.1.81"  # IP of RPI4
logger.debug(f"Host: {host}")
port = 27017
logger.debug(f"Port: {port}")
db_name = input("Enter your database name: ")
logger.debug(f"Database name: {db_name}")
collection_name = input("Enter name of collection: ")
logger.debug(f"Collection name: {collection_name}")
logger.debug(".. Finish logging user and database credentials ..")


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
                    "Choose type of field:\n1.String\n2.Integer\n3.Float\n4.UTC\n5.Exit\nChoose: "
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

logger.debug(".. Starting logging to create a fields")

while True:
    field_name = input("Name of field: ")
    logger.debug(f"Field name: {field_name}")
    field_type = choose_type_of_field()
    logger.debug(f"Field type: {field_type}")
    if field_type == 1:
        dict_of_collection.update({field_name: "str"})
        logger.debug(f"Field type: {'str'}")

    elif field_type == 2:
        value = min_max_value()
        dict_of_collection.update({field_name: ("int", value[0], value[1])})
        logger.debug(
            f"Field type: {'int'}, min value: {value[0]}, max value: {value[1]}"
        )

    elif field_type == 3:
        value = min_max_value()
        value_rounding = not_except_string("Rounding value: ")
        dict_of_collection.update(
            {field_name: ("float", value[0], value[1], value_rounding)}
        )
        logger.debug(
            f"Field type: {'float'}, min value: {value[0]}, max value: {value[1]}, rounding value: {value_rounding}"
        )
    elif field_type == 4:
        year_diff = not_except_string("Year difference: ")
        dict_of_collection.update({field_name: ("utc", year_diff)})
        logger.debug(f"Field type: {'utc'}, year difference: {year_diff}")
    elif field_type == 5:
        print("*** Field created successfully! ***\n")
        break

logger.debug(".. Finish logging to create a fields")

logger.debug(".. Start logging create of documents ..")

i = input_one_integer()
logger.debug(f"How many documents do you want to create: {i}")
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

    time.sleep(0.01)
    task.create_task(task=document_of_collection)
print("*** Documents created successfully! ***")
