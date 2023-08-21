class Author(object):
    """
    Author class

    Attributes:
        name: The author's name
        genre: The author's genre
    """

    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

        self.books = []

    def __str__(self):
        return f"{self.name}\t{self.genre}"
