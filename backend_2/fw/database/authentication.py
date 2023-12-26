class Authentication:
    def __init__(self, db):
        self.__db = db
        pass

    def signup(self, data):
        """ """
        self.__db.insert("user", data)
        return data

    def fetch_user(self, email):
        return self.__db.fetch_one("user", email=f'"{email}"')
