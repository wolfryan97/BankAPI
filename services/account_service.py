from abc import ABC, abstractmethod
from typing import List
from entities.account import Account
from entities.client import Client


class AccountService(ABC):

    # General CRUD stuff
    @abstractmethod
    def create_acct(self, acct: Account, client_id: int) -> Account:
        pass

    @abstractmethod
    def deposit(self, acct_id: int, amt: float) -> str:
        pass

    @abstractmethod
    def withdraw(self, acct_id: int, amt: float) -> str:
        pass

    @abstractmethod
    def close_acct(self, acct_id: int) -> bool:
        pass

    @abstractmethod
    def update_account(self, acct: Account) -> Account:
        pass

    @abstractmethod
    def get_acct_by_acct_id(self, acct_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> List[Account]:
        pass

    @abstractmethod
    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def transfer(self, client_id: int, acct1: int, acct2: int, amount: float) -> bool:
        pass

    @abstractmethod
    def get_accounts_in_range(self, client_id, minimum: float, maximum: float) -> List[Account]:
        pass
