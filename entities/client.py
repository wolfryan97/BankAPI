class Client:

    def __init__(self, client_id: int, client_firstname: str,
                 client_lastname: str, address: str, city: str,
                 state: str, zip_code: int):
        self.client_id = client_id
        self.client_firstname = client_firstname
        self.client_lastname = client_lastname
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        return f"Client ID: {self.client_id}\nName: {self.client_firstname} {self.client_lastname}"

    def json(self):
        return {'clientID': self.client_id,
                'firstname': self.client_firstname,
                'lastname': self.client_lastname,
                'address': self.address,
                'city': self.city,
                'state': self.state,
                'zip': self.zip_code
                }

    @staticmethod
    def json_deserialize(json):
        client = Client(0, '', '', '', '', '', '')
        client.client_id = json['clientID']
        client.client_firstname = json['firstname']
        client.client_lastname = json['lastname']
        client.address = json['address']
        client.city = json['city']
        client.state = json['state']
        client.zip_code = json['zip']
        return client
