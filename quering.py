from connect.connect import Connect
from main import TaskManager

host = "localhost"
port = 27017
db_name = input("Enter name of database: ")
collection_name = input("Enter name of collection: ")
db = TaskManager(host=host, port=port, db_name="new", collection_name="new")

while True:
    querying = int(
        input(
            "Enter number of task:\n1.Find equal value\n2.Find not equal value\n3.Find greater then\n4.Find less then\n9.Exit\nEnter: "
        )
    )

    if querying == 1:
        print("****Find equal value*****\n")
        field = input("Enter field name: ")
        value = input("Enter value: ")
        lists = db.filter_by_equals(field, value)
        for n in enumerate(lists, start=1):
            print(*n)
    elif querying == 2:
        print("****Find equal value*****\n")
        field = input("Enter field name: ")
        value = input("Enter value: ")
        lists = db.filter_by_not_equals(field, value)
        for n in enumerate(lists, start=1):
            print(*n)
    elif querying == 3:
        print("****Find greater value*****\n")
        field = input("Enter field name: ")
        value = int(input("Enter value: "))
        lists = db.filter_by_greater_than(field, value)
        for n in enumerate(lists, start=1):
            print(*n)
    elif querying == 4:
        print("****Find less value*****\n")

        lists = db.filter_by_less_than(field, value)
        for n in enumerate(lists, start=1):
            print(*n)
    elif querying == 9:
        print("Exiting")
        break
