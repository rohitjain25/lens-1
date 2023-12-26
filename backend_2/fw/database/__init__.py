import os
import sqlite3
from .authentication import Authentication


class Database:
    __authentication = None
    __DATABASENAME = "sqlite.db"
    DATA_PATH = os.path.realpath(
        os.path.dirname(os.path.realpath(__file__)) + "/../data/database"
    )

    def __init__(self, common_instance):
        self.__common_instance = common_instance
        self.__con = sqlite3.connect(self.__DATABASENAME, check_same_thread=False)
        self.__create_tables()
        self.__con = _DatabaseOperations(self.__con)

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


class _DatabaseOperations:
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
        self.__db.execute(query)
        self.__db.commit()
        pass

    def fetch_one(self, table_name, **conditions):
        try:
            condition = []
            if conditions:
                table_columns = self.table_columns(table_name)
                for key, value in conditions.items():
                    if key not in table_columns:
                        return None
                    condition.append(f"{key} = {value}")
            condition = " AND ".join(condition)
            condition = "WHERE " + condition
            query = f"select * from {table_name} {condition};"
            values = list(self.__db.execute(query).fetchone())
            data = {}
            for key, value in zip(self.table_columns(table_name), values):
                data[key] = value
            return data
        except:
            return None
