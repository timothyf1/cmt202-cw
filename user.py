class User(object):
    """
    User Class

    Attributes:
        name: The user's name
        phone_number: The user's phone number
        loan_history: A list containing the users book loan objects
    """

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

        self.loan_history = []

    def __str__(self):
        return f"{self.name} \t {self.phone_number}"
