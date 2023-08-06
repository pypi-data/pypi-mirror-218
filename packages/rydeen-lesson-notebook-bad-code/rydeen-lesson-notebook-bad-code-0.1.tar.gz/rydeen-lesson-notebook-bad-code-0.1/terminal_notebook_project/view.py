from presenter import NoteEditor

"""
user Gui for work with Note. Note creation, read Note
"""
while True:
    note_worker = NoteEditor()
    user_choice = input("""
1: Create note
2: Read note
0: Exit
Choice: """)
    if user_choice == "1":
        note_worker.create()
    if user_choice == "2":
        note_worker.read()
    if user_choice == "0":
        break
