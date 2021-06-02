from random import randint
from typing import List

from daos.account_dao import AccountDao
from entities.account import Account
from exceptions.account_not_found import AccountNotFoundError
from exceptions.insufficient_funds import InsufficientFundsError
from utils.connection_util import connection


class AccountDaoPostgres(AccountDao):

    def create_acct(self, acct: Account, client_id: int) -> Account:
        sql = """insert into account (acct_num, acct_type, balance, active, client_id) values (%s,%s,%s,%s,%s) returning acct_id"""
        cursor = connection.cursor()
        acct.acct_num = randint(1000000000, 9999999999)
        cursor.execute(sql, (acct.acct_num, acct.acct_type, acct.balance, True, client_id))
        connection.commit()
        a_id = cursor.fetchone()[0]
        acct.acct_id = a_id
        acct.client_id = client_id
        return acct

    def deposit(self, acct_id: int, amt: float) -> str:
        if amt < 0:
            return "An error occurred.\nPlease enter a value greater than 0."
        try:
            sql = """update account set balance = balance + %s where acct_id = %s returning balance"""
            cursor = connection.cursor()
            cursor.execute(sql, (amt, acct_id))
            connection.commit()
            return f"Success!\nDeposited: ${amt:.2f}\n" \
                   f"Balance: ${cursor.fetchone()[0]:.2f}"
        except TypeError:
            return "An error occurred.\nPlease enter an integer value."
        except Exception:
            raise AccountNotFoundError("Error...\nAccount does not exist")

    def withdraw(self, acct_id: int, amt: float) -> str:
        if amt < 0:
            return "Error...\nPlease enter a value greater than 0."

        sql = """update account set balance = balance - %s where acct_id = %s returning balance"""
        cursor = connection.cursor()
        cursor.execute(sql, (amt, acct_id))
        bal = cursor.fetchone()[0]
        if bal < 0:
            connection.rollback()
            return "Error...\nPlease enter a value less than the total balance."
        connection.commit()
        return f"Success!\nWithdrawn: ${amt:.2f}\n" \
               f"Balance: ${bal:.2f}"

    def close_acct(self, acct_id: int) -> bool:
        try:
            for acct in self.get_all_accounts():
                if acct.acct_id == acct_id:
                    sql = """delete from account where acct_id = %s returning acct_id"""
                    cursor = connection.cursor()
                    cursor.execute(sql, [acct_id])
                    test = cursor.fetchone()[0]
                    connection.commit()
                    return True
            connection.rollback()
            return False
        except Exception:
            raise AccountNotFoundError("Error...\nAccount does not exist")

    def update_account(self, acct: Account) -> Account:
        try:
            sql = """update account set acct_type=%s, balance=%s, active=%s, client_id=%s where acct_id=%s"""
            cursor = connection.cursor()
            cursor.execute(sql, (acct.acct_type, acct.balance, acct.active, acct.client_id, acct.acct_id))
            connection.commit()
            return acct
        except Exception:
            raise AccountNotFoundError("Error...\nAccount does not exist")

    def get_acct_by_acct_id(self, acct_id: int) -> Account:
        try:
            sql = """select * from account where acct_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [acct_id])
            records = cursor.fetchall()
            if len(records) == 0:
                raise AccountNotFoundError(f"No account of ID: {acct_id} was found.")
            for x in records:
                acct = Account(x[0], x[1], x[5], x[2], x[3], x[4])
                if x[0] == acct_id:
                    return acct
        except Exception:
            raise AccountNotFoundError("Error...\nAccount does not exist")

    def get_all_accounts(self) -> List[Account]:
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        acct_list = []
        for acct in records:
            acct = Account(acct[0], acct[1], acct[5], acct[2], acct[3], acct[4])
            acct_list.append(acct)
        return acct_list

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        sql = """select * from account where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()
        if len(records) == 0:
            return []
        acct_list = []
        for acct in records:
            acct = Account(acct[0], acct[1], acct[5], acct[2], acct[3], acct[4])
            acct_list.append(acct)
        return acct_list

    def transfer(self, client_id: int, acct1: int, acct2: int, amount: float) -> bool:
        if self.get_acct_by_acct_id(acct1).balance < amount:
            raise InsufficientFundsError("Error...Insufficient funds.")
        if self.get_acct_by_acct_id(acct1).client_id != client_id or self.get_acct_by_acct_id(
                acct2).client_id != client_id:
            raise AccountNotFoundError("Error...\nAccount does not exist")

        sql = """update account set balance = balance - %s where client_id = %s and acct_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (amount, client_id, acct1))
        connection.commit()
        sql2 = """update account set balance = balance + %s where client_id = %s and acct_id = %s"""
        cursor2 = connection.cursor()
        cursor2.execute(sql2, (amount, client_id, acct2))
        connection.commit()
        return True

    def get_accounts_in_range(self, client_id, amount_greater_than: float, amount_less_than: float) -> List[Account]:
        acct_list = self.get_accounts_by_client_id(client_id)  # will catch if client doesnt exist
        for i in range(len(acct_list) - 1, -1, -1):
            if acct_list[i].balance > amount_less_than or acct_list[i].balance < amount_greater_than:
                acct_list.pop(i)
        return acct_list
