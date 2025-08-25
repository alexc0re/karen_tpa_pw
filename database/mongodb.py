from pymongo import MongoClient
from bson.objectid import ObjectId
from env_setup import Credentials

class MongoConnection:

    def __init__(self):
        self.client = MongoClient(
            f'mongodb+srv://nemshilov90:{Credentials.DB_PASS}@cluster0.mtg98dx.mongodb.net/?retryWrites=true&w=majority'
            f'&appName=Cluster0')
        self.db = self.client['TPA']
        self.tpa_collection = self.db['tpa_table']



    def create_aroma_data(self, data):
        result = self.tpa_collection.insert_one(data)
        # print(result)
        return result

    def get_aroma_data_by_id(self):
        aroma = self.tpa_collection.find_one({"_id": ObjectId('68aaf4e02f1e3de2254632bd')})
        if aroma:
            return aroma
        else:
            raise ValueError("Aroma data not found")

    def update_aroma_data(self, data):
        result = self.tpa_collection.replace_one({"_id": ObjectId('68aaf4e02f1e3de2254632bd')}, data)
        if result.modified_count == 1:
            print("Db updated successfully.")
            return result
        else:
            print(result.raw_result)
            raise ValueError("Aroma data not updated")

    def close(self):
        self.client.close()





if __name__ == '__main__':
    db = MongoConnection()
    aromas = db.get_aroma_data_by_id()
    for aroma, prices in aromas.items():
        print(aroma, prices)
