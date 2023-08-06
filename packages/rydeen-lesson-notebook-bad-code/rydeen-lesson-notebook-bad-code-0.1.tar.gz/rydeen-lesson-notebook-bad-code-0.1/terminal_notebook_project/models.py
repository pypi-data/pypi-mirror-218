class Note:
    """
    This class for notes objects

    :param title: Note object title
    :param data: Note object creation date
    :param text: Note object text
    """

    def __init__(self,
                 title,
                 date,
                 text):
        """
        Constract method
        """
        self.title = title
        self.date = date
        self.text = text

    @property
    def show(self):
        """
        This method shows the full information that is stored
        in the Note object.  Contains the title of the note,
        the creation date and the text of the note

        :return: Returns the contents of the Note object in f-string
        :rtype: str
        """
        return f"""\nTitle: {self.text}
Date: {self.date}
Text: {self.text}"""

    @property
    def show_title(self):
        """
        This method return note title

        :return: Return Note object title
        :rtype: str
        """
        return self.title
