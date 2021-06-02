# account creation
class Account:

    def __init__(self, acct_id: int, acct_num: int, client_id: int, acct_type: str, balance: float, active: bool):
        self.acct_id = acct_id
        self.client_id = client_id
        self.acct_num = acct_num
        self.acct_type = acct_type
        self.balance = balance
        self.active = active

    def __str__(self):
        return f"Acct ID: {self.acct_id}\nAcct #: {self.acct_num}\nBalance: {self.balance}"

    def json(self):
        return {'acctID': self.acct_id,
                'clientID': self.client_id,
                'acctNum': self.acct_num,
                'acctType': self.acct_type,
                'balance': self.balance,
                'active': self.active
                }

    @staticmethod
    def json_deserialize(json):
        account = Account(0, 0, 0, '', 0, False)
        account.acct_id = json['acctID']
        account.client_id = json['clientID']
        account.acct_num = json['acctNum']
        account.acct_type = json['acctType']
        account.balance = json['balance']
        account.active = json['active']
        return account
