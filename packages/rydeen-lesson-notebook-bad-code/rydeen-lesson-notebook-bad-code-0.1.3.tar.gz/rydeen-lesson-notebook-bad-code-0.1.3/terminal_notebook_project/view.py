from presenter import get_element_number
from file_models import Database
from models import Note
from datetime import datetime


"""
user Gui for work with Note. Note creation, read Note
"""


def get_file_type():
    """
    Return type of file for saving notes in database

    :return: Return file type.
    :rtype: str
    """
    avaliable_file_types = {"1": "byte",
                            "2": "json"}
    while True:
        user_choice = input("""
Selecting the file type for saving notes:
1: Bytes
2: JSON:
Choice: """)
        if user_choice in avaliable_file_types:
            return user_choice


file_type = get_file_type()
db = Database(file_type)

while True:
    user_choice = input("""
1: Create note
2: Read note
0: Exit
Choice: """)

    if user_choice == "1":
        note = Note(title=input("Title: "),
                    date=datetime.now(),
                    text=input("Text: "))
        db.append(note)
        print("Успешно добавлено")

    if user_choice == "2":
        number = get_element_number(db.data)
        if number is not None:
            db[number].show()
    if user_choice == "0":
        break
