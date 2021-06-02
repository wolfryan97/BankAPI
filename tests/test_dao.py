from unicodedata import decimal

from daos.account_dao import AccountDao
from daos.account_dao_local import AccountDaoLocal
from daos.account_dao_postgres import AccountDaoPostgres
from daos.client_dao import ClientDao
from daos.client_dao_local import ClientDaoLocal
from daos.client_dao_postgres import ClientDaoPostgres
from entities.account import Account
from entities.client import Client

client_dao: ClientDao = ClientDaoPostgres()
acct_dao: AccountDao = AccountDaoPostgres()

# temp 0 val acct num, client, id
test_acct = Account(0, 0, 0, "Checking", 55.55, False)
test_acct2 = Account(0, 0, 0, "Savings", 40.87, False)
test_acct3 = Account(0, 0, 0, "Checking", 100.00, False)
test_acct4 = Account(0, 0, 0, "Savings", 657.22, False)
test_acct5 = Account(0, 0, 0, "Checking", 14.01, False)
test_acct6 = Account(0, 0, 0, "Savings", 4000.40, False)
test_acct7 = Account(0, 0, 0, "Checking", 1990.77, False)
test_acct8 = Account(0, 0, 0, "Savings", 657.22, False)

test_client: Client = Client(0, "Testy", "McGhee", "1234 Street St", "Woodbridge",
                             "VA", 22192)
test_client2: Client = Client(0, "Maria", "Module", "1234 Road Rd", "Woodbridge",
                              "VA", 22192)
test_client3: Client = Client(0, "Patricia", "Project", "1234 Road Rd", "Woodbridge",
                              "VA", 22192)
test_client_up: Client = Client(1, "Johnny", "Test", "1234 Street St", "Woodbridge",
                                "VA", 22192)

test_client_up2: Client = Client(10, "Darrell", "Debug", "1234 Street St", "Woodbridge",
                                 "VA", 22192)
client_dao.create_client(test_client)


# 2c 0a
class TestClientDao:

    def test_create_client(self):
        client_dao.create_client(test_client2)
        assert test_client.client_id != 0

    # 4c 0a
    def test_get_all_clients(self):
        client_dao.create_client(test_client3)
        assert len(client_dao.get_all_clients()) == 3

    def test_get_client(self):
        assert client_dao.get_client(2).client_id == test_client2.client_id

    def test_remove_client(self):
        assert client_dao.remove_client(3) is True

    # 4c 0a
    def test_update_client(self):
        assert client_dao.update_client(test_client_up) == test_client_up


class TestAccountDao:
    # successful creation
    def test_create_acct(self):
        acct_dao.create_acct(test_acct, test_client.client_id)
        assert test_acct.acct_id != 0

    # attempt depositing a valid amount
    def test_deposit(self):
        desired_output: str = f"Success!\nDeposited: $80.00\nBalance: $135.55"
        o = acct_dao.deposit(test_acct.acct_id, 80.00)
        print(desired_output)
        assert o == desired_output

    # attempt depositing a negative value
    def test_deposit2(self):
        desired_output: str = "An error occurred.\nPlease enter a value greater than 0."
        o = acct_dao.deposit(test_acct.acct_id, -10)
        assert o == desired_output

    # attempt withdrawing a valid amount
    def test_withdraw(self):
        desired_output: str = f"Success!\nWithdrawn: $44.15\nBalance: $91.40"
        o = acct_dao.withdraw(test_acct.acct_id, 44.15)
        assert o == desired_output

    # attempt withdrawing a negative amount
    def test_withdrawal2(self):
        desired_output: str = "Error...\nPlease enter a value greater than 0."
        o = acct_dao.withdraw(test_acct.acct_id, -7)
        assert o == desired_output

    # attempt withdrawing an amount greater than the balance
    def test_withdraw3(self):
        desired_output: str = "Error...\nPlease enter a value less than the total balance."
        o = acct_dao.withdraw(test_acct.acct_id, 1234.56)
        assert o == desired_output

    # attempt closing a valid acct
    def test_close_acct(self):
        assert acct_dao.close_acct(test_acct.acct_id) is True

    # attempt closing a non-valid acct
    def test_close_acct2(self):
        assert acct_dao.close_acct(9999) is False

    # attempt changing address to an acct
    def test_update_account(self):
        upd_acct = Account(test_acct2.acct_id, test_acct2.client_id, test_acct2.acct_num, "Checking", 40, False)

        the_out = acct_dao.update_account(upd_acct)

        assert the_out == upd_acct

    def test_all_accounts_by_client(self):
        test_c1: Client = client_dao.create_client(Client(0, "Peter", "Package", "1234 Street St", "Woodbridge",
                                                          "VA", 22192))
        test_a1 = acct_dao.create_acct(Account(0, 0, 0, "Checking", 55.55, False), test_c1.client_id)
        test_a2 = acct_dao.create_acct(Account(0, 0, 0, "Savings", 40, False), test_c1.client_id)
        li = [test_a1.acct_id, test_a2.acct_id]
        accts = [x for x in acct_dao.get_accounts_by_client_id(test_c1.client_id)]
        accts_cid = [y.acct_id for y in accts]
        assert accts_cid == li

    def test_transfer(self):
        test_c1: Client = client_dao.create_client(Client(0, "Timmy", "Test", "1234 Street St", "Woodbridge",
                                                          "VA", 22192))
        test_a1 = acct_dao.create_acct(Account(0, 0, 0, "Checking", 100.15, False), test_c1.client_id)
        test_a2 = acct_dao.create_acct(Account(0, 0, 0, "Savings", 75, False), test_c1.client_id)
        acct_dao.transfer(test_c1.client_id, test_a1.acct_id, test_a2.acct_id, 20)
        assert (float(acct_dao.get_acct_by_acct_id(test_a1.acct_id).balance) == float(80.15)) and (
                acct_dao.get_acct_by_acct_id(test_a2.acct_id).balance == 95)

    def test_get_accounts_in_range(self):
        accounts = acct_dao.get_accounts_in_range(5, 80, 100)
        assert len(accounts) == 2
