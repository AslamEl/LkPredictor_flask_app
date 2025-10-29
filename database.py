from pymongo import MongoClient
from config import Config

class Database:
    client = None
    db = None
    
    @staticmethod
    def initialize():
        Database.client = MongoClient(Config.MONGO_URI)
        Database.db = Database.client.get_database()
        
    @staticmethod
    def get_db():
        if Database.db is None:
            Database.initialize()
        return Database.db
    
    @staticmethod
    def close():
        if Database.client:
            Database.client.close()
