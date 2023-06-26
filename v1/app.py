import time
import random
import datetime
import lorem
from typing import Optional, Union, Tuple
from datetime import timezone, timedelta
from py_random_words import RandomWords
from tqdm import tqdm
import maskpass
from names_generator import generate_name
from connect.connect import ConnectToRpi4
from main import TaskManager


class DatabaseDataGenerator:
    def choose_type_of_field(self) -> int:
        while True:
            try:
                field_type = int(
                    input(
                        "Choose type of field:\n1.String(random words)\n2.Integer\n3.Float\n4.UTC from date now\n5.Full name\n6.Only date\n7.Random word from list of words\n8.Random number from min, max\n9.Sentence\n10.Nested\n11.Exit\nChoose: "
                    )
                )
                return field_type
            except ValueError:
                print("! -- Wrong input, must to be a number -- !", end="\n")
                continue

    def min_max_value(self) -> tuple:
        while True:
            try:
                min_value, max_value = [
                    int(x)
                    for x in input(
                        "Enter two values (min, max), separated by ',': "
                    ).split(",")
                ]
                return min_value, max_value
            except ValueError:
                print("! -- Wrong input, must to be a number -- !", end="\n")
                continue

    def random_length_number(self, min_value: int, max_value: int) -> int:
        return random.randint(min_value, max_value)

    def random_word_from_list(self, words: list) -> str:
        list_of_words = [*words]
        random_word = random.choice(list_of_words)
        return random_word

    def create_utc_datetime_min_max(
        self, difference_1: int, difference_2: int
    ) -> datetime.datetime:
        (dt := datetime.datetime.now(timezone.utc))
        min_difference = dt.year - difference_1
        max_difference = min_difference - difference_2
        rnd_years = random.randint(max_difference, min_difference)
        rnd_month = random.randint(1, 12)
        rnd_days = random.randint(1, 28)
        random_date = datetime.datetime(rnd_years, rnd_month, rnd_days)
        return random_date

    def create_utc_datetime(self, value: int) -> datetime.datetime:
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

    def not_except_string(self, string: str) -> int:
        while True:
            try:
                integer = int(input(string))
                return integer
            except ValueError:
                print("! -- Wrong input, must to be a integer -- !", end="\n")
                continue

    def input_one_integer(self):
        while True:
            try:
                i = int(input("How many documents do you want to create? "))
                return i
            except ValueError:
                print("! -- Wrong input, must to be a integer -- !", end="\n")
                continue

    def nested_field(self) -> Optional[tuple]:  # FIXME: type annotation
        while True:
            nested_field = input("Nested field, yes or no?")
            if nested_field.lower() == "yes" or nested_field.lower() == "y":
                first_field = input("First field name: ")
                choose_type_one = self.choose_type_of_field()
                second_field = input("Second field name: ")
                choose_type_second = self.choose_type_of_field()
                return first_field, choose_type_one, second_field, choose_type_second
            else:
                print("Unknown field")
                break


if __name__ == "__main":
    # * -- PROGRAM STARTS FROM HERE --
    user_name = input("Enter your database username: ")  # When use inputs
    password = maskpass.askpass(prompt="Enter your database password: ", mask="*")
    host = "192.168.1.81"  # IP of RPI4
    port = 27017
    db_name = input("Enter new database name: ")
    collection_name = input("Enter new name of database collection: ")

    db = ConnectToRpi4(
        user_name=user_name,
        user_passwd=password,
        host=host,
        port=port,
        db_name=db_name,
        collection_name=collection_name,
    )

    task = TaskManager(db)

    gen = DatabaseDataGenerator()
    dict_of_collection = {}

    while True:
        field_name = input("Name of collection field: ")

        field_type = gen.choose_type_of_field()

        if field_type == 1:
            dict_of_collection.update({field_name: "str"})

        elif field_type == 2:
            value = gen.min_max_value()
            dict_of_collection.update({field_name: ("int", value[0], value[1])})

        elif field_type == 3:
            value = gen.min_max_value()
            value_rounding = gen.not_except_string("Rounding value: ")
            dict_of_collection.update(
                {field_name: ("float", value[0], value[1], value_rounding)}
            )

        elif field_type == 4:
            year_diff = gen.not_except_string("Year difference: ")
            dict_of_collection.update({field_name: ("utc", year_diff)})

        elif field_type == 5:
            dict_of_collection.update({field_name: "fname"})

        elif field_type == 6:
            value = gen.min_max_value()
            dict_of_collection.update({field_name: ("onlydate", value[0], value[1])})

        elif field_type == 7:
            word_list = input("Write words list separated by ',': ").split(",")
            dict_of_collection.update({field_name: ("randomword", word_list)})

        elif field_type == 8:
            value = gen.min_max_value()
            dict_of_collection.update(
                {field_name: ("randominteger", value[0], value[1])}
            )

        elif field_type == 9:
            dict_of_collection.update({field_name: "sentence"})

        elif field_type == 11:
            print("*** Field created successfully! ***\n")
            break

    i = gen.input_one_integer()

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
                document_of_collection.update(
                    {keys: gen.create_utc_datetime(values[1])}
                )

            if values == "fname":  # ar reikia tik values be [0]
                document_of_collection.update({keys: generate_name(style="capital")})

            if values[0] == "onlydate":
                document_of_collection.update(
                    {keys: gen.create_utc_datetime_min_max(values[1], values[2])}
                )
            if values[0] == "randomword":
                document_of_collection.update(
                    {keys: gen.random_word_from_list(values[1])}
                )

            if values[0] == "randominteger":
                random_value = random.randint(values[1], values[2])
                document_of_collection.update({keys: random_value})

            if values == "sentence":
                sentence = lorem.get_sentence(count=2, word_range=(1, 3))
                document_of_collection.update({keys: sentence})

        time.sleep(0.01)
        task.create_task(task=document_of_collection)
    print("*** Documents created successfully! ***")
