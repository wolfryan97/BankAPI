from typing import List

from daos.account_dao import AccountDao
from entities.account import Account
from services.account_service import AccountService


class AccountServiceImpl(AccountService):

    # composition
    def __init__(self, acc_dao: AccountDao):
        self.acc_dao: AccountDao = acc_dao

    def create_acct(self, acct: Account, client_id: int) -> Account:
        acct.active = True
        return self.acc_dao.create_acct(acct, client_id)

    def deposit(self, acct_id: int, amt: float) -> str:
        return self.acc_dao.deposit(acct_id, amt)

    def withdraw(self, acct_id: int, amt: float) -> str:
        return self.acc_dao.withdraw(acct_id, amt)

    def close_acct(self, acct_id: int) -> bool:
        return self.acc_dao.close_acct(acct_id)

    def update_account(self, acct: Account) -> Account:
        return self.acc_dao.update_account(acct)

    def get_acct_by_acct_id(self, acct_id: int) -> Account:
        return self.acc_dao.get_acct_by_acct_id(acct_id)

    def get_all_accounts(self) -> List[Account]:
        return self.acc_dao.get_all_accounts()

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        return self.acc_dao.get_accounts_by_client_id(client_id)

    def transfer(self, client_id: int, acct1: int, acct2: int, amount: float) -> bool:
        return self.acc_dao.transfer(client_id, acct1, acct2, amount)

    def get_accounts_in_range(self, client_id, minimum: float, maximum: float) -> List[Account]:
        return self.acc_dao.get_accounts_in_range(client_id, minimum, maximum)
