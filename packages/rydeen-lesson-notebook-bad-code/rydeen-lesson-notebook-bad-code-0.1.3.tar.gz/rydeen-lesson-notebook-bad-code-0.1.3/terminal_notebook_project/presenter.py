def get_element_number(elements):
    """
    Returns the requested number if it passed the test.

    Calling the function Show_elements shows a list of items
    in the database.

    :param elements: List of elements from the database.
    :type elements: list
    :return: Return integet number
    :rtype: int
    """
    show_elements(elements)
    number = input("""Select a note number or \
press ENTER to go back: """)
    if number.isdigit() and 0 < int(number) <= len(elements):
        return int(number) - 1


def show_elements(elements):
    """
    Print in terminal element from database with number.
    The number is assigned using enumerate.
    Report in enumerate starts from 1

    :param elements: List of elements from the database.
    :return: None
    :rtype: NoneType
    """
    for number, element in enumerate(elements, 1):
        print(f"\n{number}: {element}")
        print("-"*20)
