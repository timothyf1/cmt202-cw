class BookLoan(object):
    """
    Bookloan Class

    Attributes:
        book: The book object which the loan is for
        user: The user object who loans the book
        loan_start: The date which the loan started on
        loan_end: The date which the loan ended on
        active: A boolean for if this loan is currently active

    Methods:
        end_loan: Sets the end loan date and sets active to false
    """

    def __init__(self, book, user, loan_start):
        self.book = book
        self.user = user
        self.loan_start = loan_start
        self.active = True

    def end_loan(self, loan_end):
        """
        Methods to end a book loan

        Returns:
            1 if book loan has ended
            0 if end date is before start date
        """

        if loan_end < self.loan_start:
            return 0
        self.loan_end = loan_end
        self.active = False
        return 1
