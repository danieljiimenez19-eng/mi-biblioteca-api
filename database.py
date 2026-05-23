from pymongo import MongoClient

MONGO_URI = "mongodb+srv://danieljiimenez_db_user:nBu0LB6jKH3yPNS9@cluster0.y8rtppz.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["biblioteca"]
books_collection = db["books"]