import datetime

from Pyro5.api import expose, behavior, serve, Daemon

from author import Author
from book import Book
from bookloan import BookLoan
from user import User

@expose
@behavior(instance_mode="single")
class library(object):
    def __init__(self):
        self.authors = []
        self.books = []
        self.users = []
        self.loans = []

    def get_user(self, user_name):
        """
        Method to find the user object for a given username
        """
        for user in self.users:
            if user.name == user_name:
                return user
        return None

    def get_author(self, name):
        """
        Method to find the author object for a given author name
        """
        for author in self.authors:
            if author.name == name:
                return author
        return None

    def get_book(self, title):
        """
        Method to find the book object for a given book title
        """
        for book in self.books:
            if book.title == title:
                return book
        return None

    def get_loan(self, book, user):
        """
        Method to find if a user with a given username has already loaned a given book
        """
        for loan in self.loans:
            if loan.user == user and loan.book == book:
                return loan
        return None

    def table_to_string(self, table):
        """
        Method to convert a table of nested list to a string to send and output
        """
        num_of_cols = len(table[0])
        col_max_length = [max([len(str(elem)) for elem in col]) for col in list(map(list, zip(*table)))]
        table.insert(1, ["-" * i for i in col_max_length])

        string = ""
        for row in table:
            rowstring = ""
            for i in range(num_of_cols):
                rowstring += "{0:<{1}} | ".format(row[i], col_max_length[i])
            string += f"{rowstring[:-2].strip()}\n"
        return string

    def add_user(self, user_name, user_number):
        """
        Task 1
        Method to add a new user to the library
        """
        if user_name not in [user.name for user in self.users]:
            self.users.append(User(user_name, user_number))
            return 1
        return 0

    def return_users(self):
        """
        Task 2
        Method to return all users of the library
        """
        # Check to see if there are any users
        if len(self.users) == 0:
            return "There are currently no users in the library\n"

        table = [["User Name", "Contact Number"]]
        for user in self.users:
            table.append([user.name, user.phone_number])
        return "The following users are in the library\n" + self.table_to_string(table)

    def add_author(self, author_name, author_genre):
        """
        Task 3
        Method to add a new book author to the library
        """
        if author_name not in [author.name for author in self.authors]:
            self.authors.append(Author(author_name, author_genre))
            return 1
        return 0

    def return_authors(self):
        """
        Task 4
        Method to return all authors in the library
        """
        if len(self.authors) == 0:
            return "There are currently no authors in the library\n"

        table = [["Author Name", "Genre"]]
        for author in self.authors:
            table.append([author.name, author.genre])
        return "The following authors are in the library\n" + self.table_to_string(table)

    def add_book_copy(self, author_name, book_title):
        """
        Task 5
        Add a book to the library
        """
        author = self.get_author(author_name)

        if author:
            book = self.get_book(book_title)
            if book:
                book.copies += 1
            else:
                book = Book(book_title, author)
                self.books.append(book)
                author.books.append(book)
            return 1

        return 0

    def return_books_not_loan(self):
        """
        Task 6
        List of books not on loan
        """
        table = [["Author", "Title", "Copies Available"]]
        for book in self.books:
            if (copies := book.copies_available(self.loans)) > 0:
                table.append([book.author.name, book.title, copies])

        if len(table) > 1:
            return "The following books are available for loan\n" + self.table_to_string(table)

        return "There are currently no books available to loan\n"

    def loan_book(self, user_name, book_title, year, month, day):
        """
        Task 7
        Loan a book
        """
        book = self.get_book(book_title)
        user = self.get_user(user_name)

        if book and user:
            # Check to see if the user already has this book on loan
            if self.get_loan(book, user):
                return 0

            # Check to see if there is a copy available to loan
            if book.copies_available(self.loans) > 0:
                loan = BookLoan(book, user, datetime.date(year, month, day))
                user.loan_history.append(loan)
                self.loans.append(loan)
                return 1

        return 0

    def return_books_loan(self):
        """
        Task 8
        Return list of books on loan
        """
        if len(self.loans) == 0:
            return "There are currently no books on loan\n"

        table = [["Book", "Author", "Loaned to"]]
        for loan in self.loans:
            table.append([loan.book.title, loan.book.author.name, loan.user.name])
        return "The following books are currenlty on loan\n" + self.table_to_string(table)

    def end_book_loan(self, user_name, book_title, year, month, day):
        """
        Task 9
        User returns book to libary.
        """
        book = self.get_book(book_title)
        user = self.get_user(user_name)

        if user and book:
            if loan := self.get_loan(book, user):
                if loan.end_loan(datetime.date(year, month, day)) == 1:
                    self.loans.remove(loan)
                    return 1

        return 0

    def delete_book(self, book_title):
        """
        Task 10
        Remove book from library
        """
        if book := self.get_book(book_title):
            copies_not_loaned = book.copies_available(self.loans)
            if copies_not_loaned == book.copies:
                self.books.remove(book)
            else:
                book.copies -= copies_not_loaned

    def delete_user(self, user_name):
        """
        Task 11
        Remove a user from the library
        """
        if user := self.get_user(user_name):

            # Check to see if the user has never loaned a book
            if len(user.loan_history) == 0:
                self.users.remove(user)
                return 1

        return 0

    def user_loans_date(self, user_name, start_year, start_month,
                        start_day, end_year, end_month, end_day):
        """
        Task 12
        Return a users completed book loans
        """
        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)

        if user := self.get_user(user_name):
            table = [["Book", "Author", "Loan Start", "Loan End"]]
            for loan in user.loan_history:
                if not loan.active:
                    if start_date <= loan.loan_start and loan.loan_end <= end_date:
                        table.append([loan.book.title, loan.book.author.name, str(loan.loan_start), str(loan.loan_end)])

            if len(table) > 1:
                return f"{user_name} has loaned the following books between the provided dates\n" + self.table_to_string(table)
            return f"There are no loans for {user_name} within the provided dates.\n"

        return f"The user {user_name} does not exsist in the library.\n"


if __name__=="__main__":
    daemon = Daemon()
    serve({library: "example.library"}, daemon=daemon, use_ns=True)
