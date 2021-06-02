import random
from typing import List

from daos.account_dao import AccountDao
from entities.account import Account
from exceptions.account_not_found import AccountNotFoundError
from exceptions.insufficient_funds import InsufficientFundsError


class AccountDaoLocal(AccountDao):
    acct_maker = 0
    acct_table = {}
    id_maker = 0

    def create_acct(self, acct: Account, client_id: int) -> Account:
        AccountDaoLocal.acct_maker = random.randint(1000000000, 9999999999)
        acct.acct_num = AccountDaoLocal.acct_maker
        AccountDaoLocal.id_maker += 1
        acct.acct_id = AccountDaoLocal.id_maker
        acct.client_id = client_id
        # add item to dictionary
        AccountDaoLocal.acct_table[acct.acct_id] = acct
        acct.active = True
        return acct

    def deposit(self, acct_id: int, amt: float) -> str:
        try:
            # negative deposit
            if amt < 0:
                return "An error occurred.\nPlease enter a value greater than 0."
            elif acct_exists(self.acct_table, acct_id) is False:
                return "An error occurred.\nPlease enter a valid account number."
            # valid output here
            else:
                AccountDaoLocal.acct_table[acct_id].balance += amt
                return f"Success!\nDeposited: ${amt:.2f}\n" \
                       f"Balance: ${AccountDaoLocal.acct_table[acct_id].balance:.2f}"

        except TypeError:
            return "An error occurred.\nPlease enter an integer value."
        except ValueError:
            return "An error occurred.\nPlease enter a valid account number."

    def withdraw(self, acct_id: int, amt: float) -> str:
        # "Success!\nWithdrawn: $44.15\nBalance: $91.40"
        try:
            # negative withdrawal
            if amt < 0:
                return "An error occurred.\nPlease enter a value greater than 0."
            elif amt > AccountDaoLocal.acct_table[acct_id].balance:
                return "An error occurred.\nPlease enter a value less than the total balance."
            elif acct_exists(self.acct_table, acct_id) is False:
                return "An error occurred.\nPlease enter a valid account number."
            # valid output here
            else:
                AccountDaoLocal.acct_table[acct_id].balance -= amt
                return f"Success!\nWithdrawn: ${amt:.2f}\n" \
                       f"Balance: ${AccountDaoLocal.acct_table[acct_id].balance:.2f}"

        except TypeError:
            return "An error occurred.\nPlease enter an integer value."
        except ValueError:
            return "An error occurred.\nPlease enter a valid account number."

    def close_acct(self, acct_id: int) -> bool:
        try:
            if acct_exists(self.acct_table, acct_id) is False:
                return False
            else:
                self.acct_table.pop(acct_id)
                return True
        except KeyError:
            return False

    def update_account(self, acct: Account) -> Account:
        try:
            AccountDaoLocal.acct_table[acct.acct_id] = acct
            return acct
        except KeyError:
            raise AccountNotFoundError("An error occurred.\nPlease enter valid account information.")

    def get_acct_by_acct_id(self, acct_id: int) -> Account:
        try:
            return self.acct_table[acct_id]
        except KeyError:
            raise AccountNotFoundError("An error occurred. Account not found.")

    def get_all_accounts(self) -> List[Account]:
        return list(AccountDaoLocal.acct_table.values())

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        li = []
        for acct in list(AccountDaoLocal.acct_table.values()):
            if acct.client_id == client_id:
                li.append(acct)
        return li

    def transfer(self, client_id: int, acct1: int, acct2: int, amount: float) -> bool:
        # client doesnt have both accounts
        if self.get_acct_by_acct_id(acct1).client_id != client_id or \
                self.get_acct_by_acct_id(acct2).client_id != client_id:
            raise AccountNotFoundError("An error occurred.\nPlease enter valid account information.")
        # not enough funds
        if self.get_acct_by_acct_id(acct1).balance < amount:
            raise InsufficientFundsError("Error...Insufficient funds.")
        # success
        self.get_acct_by_acct_id(acct1).balance -= amount
        self.get_acct_by_acct_id(acct2).balance += amount
        return True

    def get_accounts_in_range(self, client_id, amount_greater_than: float, amount_less_than: float) -> List[Account]:
        li = self.get_accounts_by_client_id(client_id)
        out = []
        for acct in li:
            if amount_greater_than <= acct.balance <= amount_less_than:
                out.append(acct)
        return out

# helper function
def acct_exists(d: dict, acct_id: int) -> bool:
    if d[acct_id] is not None:
        return True
