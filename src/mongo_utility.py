from pymongo import MongoClient
import os
import configparser

mongo_client = None

class mongo_utility:

    def __init__(self, app):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        self.DEFAULT_MONGO_URI =parser.get('DEFAULT','mongo_url')
        self.db = parser.get('DEFAULT','database_name')
        self.collection = parser.get('DEFAULT','collection_name')
        self.app = app

    def __get__mongo_client(self):
        global mongo_client
        # checking if MongoURI is already set

        if 'MONGO_URI' not in self.app.config:
            self.app.config['MONGO_URI'] = os.getenv('MONGO', self.DEFAULT_MONGO_URI)

        # checking if mongo client is already set
        if not mongo_client:
            mongo_client = MongoClient(self.app.config['MONGO_URI'])

        return mongo_client

    def insert_document(self, data):
        return self.__get__mongo_client()[self.db][self.collection].insert_one(data)

    def get_document(self, data):
        return self.__get__mongo_client()[self.db][self.collection].find_one(data)

    def get_documents(self, query, column_query):
        return self.__get__mongo_client()[self.db][self.collection].find(query, column_query)

    def update_documents(self, query, column_value):
        return self.__get__mongo_client()[self.db][self.collection].update_many(query, column_value)
