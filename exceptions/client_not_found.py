class ClientNotFoundError(Exception):

    description: str = 'Occurs when a client is not found'

    def __init__(self, message: str):
        self.message = message

