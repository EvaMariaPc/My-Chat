from pymongo import MongoClient
from bson import ObjectId
from pymongo.server_api import ServerApi
import logging
import json
from pymongo import MongoClient
from bson.objectid import ObjectId


def connect_to_mongodb():
    try:
        uri = "mongodb+srv://purtuceva2004:stefaniubi09@cluster0.8hmaibk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client["flight_deals"]
        logging.info('Connected to MongoDB successfully')
        return db
    except Exception as e:
        logging.error(f'Failed to connect to MongoDB: {e}')
        raise


def insert_data_to_mongodb(data):
    client = connect_to_mongodb()
    print(f"connected:{client}")
    db = client.flight_deals
    print(f"db:{db}")

    # Define collections
    deals_collection = db.deals
    destinations_collection = db.destinations
    departure_collection = db.departure
    print(f"deals,destination,departure:{destinations_collection,deals_collection,departure_collection}")

    for flight in data['Flights']:
        # Insert into destinations collection
        destination_doc = {
            "name": flight["Destination"]
        }
        print(f"destination deocument:{destination_doc}")
        destination_result = destinations_collection.insert_one(destination_doc)
        print(f"destination result:{destination_result}")
        destination_id = destination_result.inserted_id
        print(f"destination:{destination_id}")

        # Insert into departure collection
        departure_doc = {
            "name": flight["Departure"]
        }
        departure_result = departure_collection.insert_one(departure_doc)
        departure_id = departure_result.inserted_id
        print(f"departure:{departure_id}")

        # Insert into deals collection
        deals_doc = {
            "departure_id": departure_id,
            "destination_id": destination_id,
            "price": flight["Flight_price"]
        }
        deals_collection.insert_one(deals_doc)

    print("Data inserted successfully")


file_path = 'flights_data.json'  # Ensure this path is correct
with open(file_path, 'r', encoding='utf-8') as json_file:
    flight_data = json.load(json_file)