from datetime import datetime
from file_models import DataBase
from models import Note


class NoteEditor:
    """
    This class edits the Note class

    :param db: Get link to data base by class: `DataBase`
    :type db: list
    :param date: Get current date by datetitme
    :type date: str
    """

    def __init__(self):
        """
        Constructor method
        """

        self.db = DataBase("db.txt")
        self.date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    def is_valid_number(self):
        """
        Returns an integer after getting and validating,
        otherwise returns None

        :return: int
        :rtype: int
        """
        number = input("""Select a note number or \
press ENTER to go back: """)
        if number.isdigit() and 0 < int(number) <= len(self.db):
            return int(number) - 1

    def create(self):
        """
        This method creates record in the database

        :return: None
        :rtype: NoneType
        """
        data = Note(title=input("Note title: "),
                    date=self.date,
                    text=input("Note Text: "))

        self.db.append(data)

    def show(self):
        """
        This method retrieves all records from the database and give number.
        The number of records and headings is displayed in the terminal

        :return: None
        :rtype: NoneType
        """
        if self.db.data:
            for number, el in enumerate(self.db.data, 1):
                print(f"\n{number}: {el.show_title}")
                print("-"*20)
        else:
            print("="*21)
            print("  Database empty")
            print("="*21)

    def read(self):
        """
        Тhis method reads the record from the database by the received
        number and output to the terminal.

        :return: None
        :rtype: NoneType
        """

        self.show()
        if self.db.data:
            number = self.is_valid_number()
            if number is not None:
                print(self.db[number].show)
