import json
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

    def get_enum_keys(self, cls):
        keys = []
        for key in vars(cls).keys():
            if not((key.startswith('__')) and key.endswith('__')):
                keys.append(key)
        return keys

    def get_enum_values(self, cls):
        values = []
        dummy_data =vars(cls)
        for key in dummy_data.keys():
            if not((key.startswith('__')) and key.endswith('__')):
                values.append(dummy_data[key])
        return values
                
