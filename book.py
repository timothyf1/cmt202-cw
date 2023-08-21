class Book(object):
    """
    Book Class

    Attributes:
        title: The book's name
        author: The author object of the book
        copies: The number of copies of the book in the library

    Methods:
        copies_available: Returns the number of the books which are not on loan
    """

    def __init__(self, title, author):
        self.title = title
        self.author = author

        # Initialize the book in the library system with 1 copy
        self.copies = 1

    def copies_available(self, loans):
        book_loans = [loan for loan in loans if loan.book == self]
        return self.copies - len(book_loans)

    def __str__(self):
        return f"{self.title}\t{self.author.name}\t{self.copies} copies"
