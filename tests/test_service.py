from unittest.mock import MagicMock

from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao_local import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres
from entities.account import Account
from entities.client import Client
from services.account_service_impl import AccountServiceImpl
from services.client_service_impl import ClientServiceImpl

test_acct = Account(0, 0, 0, "Checking", 55.55, False)
test_acct2 = Account(0, 0, 0, "Savings", 40, False)
test_acct3 = Account(0, 0, 0, "Checking", 100, False)
accounts = [test_acct, test_acct2, test_acct3]

test_client: Client = Client(0, "Bob", "Jones", "1234 Street St", "Woodbridge",
                             "VA", 22192)
test_client2: Client = Client(0, "Timmy", "Turner", "1234 Street St", "Woodbridge",
                              "VA", 22192)
test_client_up: Client = Client(1, "Bob", "Jones", "1234 Road Rd", "Woodbridge",
                                "VA", 22192)
clients = [test_client, test_client2]

mock_account_dao = AccountDaoLocal()
mock_client_dao = ClientDaoLocal()
mock_account_dao.get_all_accounts = MagicMock(return_value=accounts)
mock_client_dao.get_all_clients = MagicMock(return_value=clients)
account_service = AccountServiceImpl(mock_account_dao)
client_service = ClientServiceImpl(mock_client_dao)


class TestAccountService:
    def test_create_client(self):
        client_service.create_client(clients[0])
        client_service.create_client(clients[1])
        assert len(client_service.get_all_clients()) == 2

    def test_create_acct(self):
        account_service.create_acct(accounts[0], 1)
        account_service.create_acct(accounts[1], 1)
        account_service.create_acct(accounts[2], 2)
        assert len(account_service.get_all_accounts()) == 3

    def test_update_client(self):
        client_service.update_client(test_client_up)
        assert client_service.get_client(1).address == "1234 Road Rd"

    def test_update_acct(self):
        test_acct_up = Account(2, mock_account_dao.get_acct_by_acct_id(2).acct_num, 1, "Checking", 55.55, True)
        account_service.update_account(test_acct_up)
        assert account_service.get_acct_by_acct_id(2).acct_type == "Checking"
