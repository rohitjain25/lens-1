from fastapi import Response


class Authentication:
    __table_name = "user"
    
    def __init__(self, db):
        self.__db = db
        pass

    def signup(self, data, response:Response):
        """ """
        db_response = self.__db.insert(self.__table_name, data)
        if not db_response:
            del data["password"]
            response.status_code = 201
            return data, response
        else:
            response.status_code = 409
            return {"error": db_response}, response

    def fetch_user(self, email):
        return self.__db.fetch_one(self.__table_name, [{"key":"email", "value":f'{email}', "type": "string"}])

    def delete(self, email):
        return self.__db.delete(self.__table_name, [{"key":"email", "value":f'{email}', "type": "string"}])
