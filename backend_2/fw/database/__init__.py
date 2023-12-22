import os, json
import sqlite3
class Database:
    DATA_PATH = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+ "/../data/database")
    def __init__(self):
        print(self.DATA_PATH)
        queries = json.load(open(self.DATA_PATH+'/query.json','r'))["creating_tables"]
        
        self.con = sqlite3.connect('sqlite.db')
        for query in queries.items():
            self.con.execute(query[1])
        
        
        