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

    def show(self):
        """
        This method shows the full information that is stored
        in the Note object.
        Contains:
            Note title;
            Date of creation:
            Note text.

        :return: None
        :rtype: NoneType
        """
        print(f"""\nTitle: {self.text}
Date: {self.date}
Text: {self.text}""")

    def __str__(self):
        """
        Return title of class object

        :return: Return objectvtitle
        :rtype: str
        """
        return self.title
