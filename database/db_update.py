# *** DB fixtures ***
import json

import pytest

from data import data as aromas_data
from database.db_connection import DataBaseConnection
from env_setup import Credentials


class AromasDB:

    def __init__(self):
        self.db_connection = DataBaseConnection(
            dbname="uzpeqkka",
            user="uzpeqkka",
            password=Credentials.DB_PASS,
            host="trumpet.db.elephantsql.com",
            port="5432")


    def create_aroma_data(self):
        data = aromas_data
        cur = self.db_connection.connection.cursor()
        cur.close()
        aroma_data = json.dumps(data)
        self.db_connection.execute(
            "INSERT INTO tpa_table (aromas_data)  VALUES (%s)",
            aroma_data)

        self.db_connection.connection.commit()


    def update_aroma_data(self , data, id=2):
        new_data = json.dumps(data)
        query = "UPDATE tpa_table SET aromas_data = %s WHERE id = %s"
        self.db_connection.execute(query, new_data, id)
        self.db_connection.connection.commit()


    def get_aroma_data_by_id(self, id=2):
        query = "SELECT aromas_data FROM tpa_table WHERE id = %s"
        row = self.db_connection.fetchone(query, id)
        return row