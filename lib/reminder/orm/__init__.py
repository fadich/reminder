import os
import pymongo

from reminder.functional.decorators import cashed_property


HOST = os.environ.get('MONGO_HOST', '0.0.0.0')
PORT = int(os.environ.get('MONGO_PORT', 27017))
USERNAME = os.environ.get('MONGO_USERNAME')
PASSWORD = os.environ.get('MONGO_PASSWORD')


@cashed_property()
def client():
    return pymongo.MongoClient(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD)


def get_collection(name: str) -> pymongo.collection.Collection:
    return getattr(client.db, name)
