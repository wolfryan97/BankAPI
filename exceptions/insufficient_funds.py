class InsufficientFundsError(Exception):

    description: str = 'Insufficient funds during transfer'

    def __init__(self, message: str):
        self.message = message
