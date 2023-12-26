import json


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
