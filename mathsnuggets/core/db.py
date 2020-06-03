import pymongo

client = pymongo.MongoClient("localhost", 27017)
slideshows = client.mathsnuggets.slideshows
