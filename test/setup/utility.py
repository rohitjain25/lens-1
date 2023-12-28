import json
import os
from openapi_schema_validator import validate


class Utility:
    def load_file(self, data_path, filename):
        """
        This function is to read a json file and return it in dict format.
        Parameters :
            data_path: Actual path to the file's folder
            filename: Name of the file (with extension)
        Return: Returns a dictonary
        """

        data = json.load(open(data_path + "/" + filename, "r"))
        return data

    def response_validator(self, response, schema_filename):
        Schema_Dir_Path = os.path.realpath(
            os.path.dirname(os.path.realpath(__file__)) + "/../tests/backend/schemas"
        )
        schema = self.load_file(Schema_Dir_Path, schema_filename)
        validate(response, schema)
        return  True