from pymongo import MongoClient
from pymongo.errors import OperationFailure

client = MongoClient("mongodb://ufo:pempiai234@192.168.1.81/")
db = client["exercise_db"]
collection = db["exercise_collection"]

validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "age": {
                    "bsonType": "int",
                    "minimum": 18,
                    "maximum": 99,
                    "description": "Age must be an integer between 18 and 90.",
                },
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "description": "Email must be a valid email address.",
                },
            },
        },
    },
}

# Create the collection with schema validation
# collection.create_index([("name", 1)], unique=True)  # Optional: Add unique index
# collection.create_index(
#     validation_rules, {"validator": {"$jsonSchema": validation_rules}}
# )

# Set the validation rules for the collection
# try:
#     db.command("collMod", collection.name, **validation_rules)
#     print("Schema validation enabled.")
# except OperationFailure as e:
#     print(f"Failed to enable schema validation: {e.details['errmsg']}")

# # Clean up (optional)
# client.close()


# Insert a document that satisfies the validation rules
valid_doc = {"name": "Tadas Blinda", "age": 30, "email": "tadasblinda@gmail.com"}
collection.insert_one(valid_doc)

# # # Insert a document that violates the validation rules
# invalid_doc = {
#     "name": "Tadas Blinda",
#     "age": "25",  # Invalid data type
#     "email": "janesmith",  # Invalid email format
# }
# try:
#     collection.insert_one(invalid_doc)
# except Exception as e:
#     print(f"Failed to insert document: {e}")

# # Retrieve all documents from the collection
# documents = collection.find()
# for doc in documents:
#     print(doc)

# collection.drop()
# db.command("collMod", collection.name, **validation_rules)
