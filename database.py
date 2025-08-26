from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DB_NAME]

risk_analysis_collection = db["risk_analyses"]

def save_analysis(analysis_data):
    return risk_analysis_collection.insert_one(analysis_data)

def get_analysis_history():
    return list(risk_analysis_collection.find({}, {"_id": 0}))
