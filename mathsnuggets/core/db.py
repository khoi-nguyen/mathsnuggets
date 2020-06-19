import os

import pymongo

url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
client = pymongo.MongoClient(url)
slideshows = client.mathsnuggets.slideshows
collections = client.mathsnuggets
