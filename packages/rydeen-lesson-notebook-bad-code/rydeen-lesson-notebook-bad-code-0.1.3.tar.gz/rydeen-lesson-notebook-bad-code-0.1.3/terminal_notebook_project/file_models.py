import os
import pickle
import jsonpickle


class FileService:
    """
    The File Service class reads/uploads files with the given name.
    Uses the PICKLE library to serialize data

    :param filename: File name to read or write
    """

    def __init__(self,
                 filename):
        """
        Constract method

        Check for the existence of the pickle file and create a new
        one if not found.
        """
        self.__filename = filename
        if not os.path.exists(filename):
            self.write([])

    def read(self):
        """
        This method read pickle file

        :return: List of data
        :rtype: list
        """
        with open(self.__filename, "rb") as f:
            return pickle.loads(f.read())

    def write(self, data):
        """
        This method write data to pickle file

        :param data: Some data for write in file
        :return: None
        """
        with open(self.__filename, "wb") as f:
            f.write(pickle.dumps(data))


class FileJsonService:
    """
    The File Service class reads/uploads files with the given name.
    Uses the JSON library to serialize data

    :param filename: File name to read or write
    """

    def __init__(self,
                 filename):
        """
        Constract method

        Check for the existence of the JSON file and create a new
        one if not found
        """
        self.__filename = filename
        if not os.path.exists(filename):
            self.write([])

    def read(self):
        """
        This method read JSON file

        :return: List of data
        :rtype: list
        """
        with open(self.__filename, "r") as f:
            return jsonpickle.decode(f.read())

    def write(self, data):
        """
        This method write data to pickle file

        :param data: Some data for write in file
        :return: None
        :rtype: NoneType
        """
        with open(self.__filename, "w") as f:
            f.write(jsonpickle.encode(data))


class Database:
    """
    This class works with the database

    :param filename: Get name of file to work
    :type: str
    :param mode: With what type of file mast work data base. Default = byte
    :type: str, optional
    :param fileservice: Get type of fileservice class from fileservice
    dictionary.
    [mode] - type of class fileservice:
    (class: `FileService` - pickle fileservice
     class: 'FileJsonService' - JSON fileservice)
    :type: class
    :param data: Read database data from file by fileservice
    :type: object

    """

    def __init__(self,
                 filename,
                 mode="byte"):
        """
        Constarct method
        """
        fileservice = {
            "byte": FileService,
            "json": FileJsonService}
        self.fileservice = fileservice[mode](filename)

        self.data = self.fileservice.read()

    def save(self):
        """
        Save data to data base file
        """
        self.fileservice.write(self.data)

    def append(self, data):
        """
        Append data to database

        :param data: Data to append in database
        :type: class
        """
        self.data.append(data)
        self.save()

    def pop(self, element):
        """
        Delete data from data base by index number

        :param element: Index of element to delete from database list
        """
        self.data.pop(element)

    def remove(self, element):
        """
        Delete data from data base by index number

        :param element: Index of element to delete from database list
        """
        self.data.remove(element)
        self.save()

    def clear(self):
        """
        Clear all data base
        """
        self.data.clear()
        self.save()

    def __len__(self):
        """
        Return data base lenght

        :return: Return database lenght
        :rtype: int
        """
        return len(self.data)

    def __getitem__(self, number):
        """
        Get element from database by index number

        :return: Return element from database by number
        :rtype: class
        """
        return self.data[number]

    def __str__(self):
        """
        Show database

        :return: Return object selected class
        :rtype: object
        """
        return f"{self.data}"
