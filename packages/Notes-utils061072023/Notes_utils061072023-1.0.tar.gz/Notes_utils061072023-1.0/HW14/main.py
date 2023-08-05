class Note:
    """
    class Note. Represents a note with a title and text.

    :param title: The title of the note..
    :type: str
    :param text: The text of the note.
    :type: str
    """
    def __init__(self, title, text):
        """ Initialized Method
        """
        self.title = title
        self.text = text

    def show_note(self):
        """
        Metod show_note. Displays the title and text of the note.
        """
        print("Title:", self.title)
        print("Text:", self.text)


class Notebook:
    """
    class Notebook. Represents a collection of notes.
    """
    def __init__(self):
        """
        Initialized Method. Initializes a new instance of the Notebook class.
        """
        self.notes = []

    def add_note(self, title, text):
        """
        Method add_notes. Adds a new note to the notebook.
        
        :param title: The title of the note.
        :type: str
        :param text: The text of the note.
        :type: str
        
        """
        self.notes.append(Note(title, text))

    def show_notes(self):
        """
        Method show_notes. Displays all the notes in the notebook.
        """
        if not self.notes:
            print("В блокноте нет заметок")
        else:
            print("Заметка:")
            for note in self.notes:
                note.show_note()

    def read_note(self, index):
        """
        Method read_note. Reads a note from the notebook
        based on the given index.

        :param index: The index of the note to read.
        :type: int
        """
        if 0 <= index < len(self.notes):
            note = self.notes[index]
            note.show_note()
        else:
            print("Заметка не существует.")

          
