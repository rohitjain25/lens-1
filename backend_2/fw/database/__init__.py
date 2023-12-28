import os
import copy
import sqlite3
from pymongo import MongoClient
from .authentication import Authentication


class Database:
    __DATABASETYPE = "sqlite3"
    __authentication = None
    __DATABASENAME = "sqlite.db"
    __CONNECTION_STRING = (
        "mongodb+srv://lens_rw:hCFgvYUeY62LHeJ3@lens-mdb.ljxkjx4.mongodb.net/"
    )
    DATA_PATH = os.path.realpath(
        os.path.dirname(os.path.realpath(__file__)) + "/../data/database"
    )

    def __init__(self, common_instance):
        self.__common_instance = common_instance
        if self.__DATABASETYPE == "sqlite3":
            self.__con = sqlite3.connect(self.__DATABASENAME, check_same_thread=False)
            self.__create_tables()
            self.__con = _Sqlite3_Client(self.__con)
        elif self.__DATABASETYPE == "mongodb":
            self.__con = _MongoDB_CLient(self.__CONNECTION_STRING)

    def __create_tables(self):
        queries = self.__common_instance.utility.load_file(
            self.DATA_PATH, "query.json"
        )["creating_tables"]
        for query in queries.items():
            self.__con.execute(query[1])

    @property
    def authentication(self):
        if self.__authentication is None:
            self.__authentication = Authentication(self.__con)
        return self.__authentication


class _Sqlite3_Client:
    def __init__(self, db):
        self.__db = db

    def table_columns(self, table_name):
        columns = []
        for column in self.__db.execute(f"PRAGMA table_info({table_name});"):
            columns.append(column[1])
        return columns

    def insert(self, table_name, data):
        query = "INSERT INTO {} ({}) VALUES {};"
        values = tuple([f"{value}" for value in data.values()])
        query = query.format(table_name, ", ".join(data.keys()), values)
        try:
            self.__db.execute(query)
            self.__db.commit()
        except Exception as e:
            return ("Error while inserting into {}:".format(table_name), e)

    def __generate_condition(self, conditions):
        condition_list = []
        condition_str = ""
        for condition in conditions:
            condition_instance_str = condition["key"] + " = "
            if condition["type"] == "string":
                condition["value"] = '"' + str(condition["value"]) + '"'
            condition_instance_str += condition["value"]
            condition_list.append(condition_instance_str)
        if len(condition_list) > 0:
            condition_str = "WHERE " + " AND ".join(condition_list)
        return condition_str

    def fetch_one(self, table_name, conditions=[]):
            condition = self.__generate_condition(conditions)
            query = f"select * from {table_name} {condition};"
            values = list(self.__db.execute(query).fetchone())
            data = {}
            for key, value in zip(self.table_columns(table_name), values):
                data[key] = value
            return data

    def delete(self, table_name, conditions=[]):
        try:
            condition = self.__generate_condition(conditions)
            query = f"DELETE from {table_name} {condition};"
            values = list(self.__db.execute(query))
            self.__db.commit()
            data = {}
            for key, value in zip(self.table_columns(table_name), values):
                data[key] = value
            return data
        except Exception as e:
            return None


class _MongoDB_CLient:
    def __init__(self, connection_string):
        self.__client = MongoClient(connection_string)
        self.__client = self.__client["lens_db"]

    def table_columns(self, table_name):
        pass

    def insert(self, table_name, data, conditions=None):
        try:
            self.__client[table_name].insert_one(copy.deepcopy(data))
        except Exception as e:
            return {"error": e}

    def fetch_all(self, table_name, conditions):
        return [data for data in self.__client[table_name].find(conditions)]

    def fetch_one(self, table_name, **conditions):
        print(conditions)
        return self.__client[table_name].find_one(conditions)

    def delete(self, table_name, **conditions):
        pass
