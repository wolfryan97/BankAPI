class AccountNotFoundError(Exception):

    description: str = 'Occurs when an account is not found'

    def __init__(self, message: str):
        self.message = message

