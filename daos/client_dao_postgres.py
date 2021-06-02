from typing import List

from daos.client_dao import ClientDao
from entities.client import Client
from exceptions.client_not_found import ClientNotFoundError
from utils.connection_util import connection


class ClientDaoPostgres(ClientDao):
    # DEBUG
    print("CONNECTION:", connection)


    def create_client(self, client: Client) -> Client:
        sql = """insert into client (client_firstname, client_lastname, address, city, state, zip_code) values (%s,%s,%s,%s,%s,%s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (
            client.client_firstname, client.client_lastname, client.address, client.city, client.state,
            client.zip_code))
        connection.commit()
        c_id = cursor.fetchone()[0]
        client.client_id = c_id
        return client

    def get_all_clients(self) -> List[Client]:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        client_list = []
        for client in records:
            client = Client(client[0], client[1], client[2], client[3], client[4], client[5], client[6])
            client_list.append(client)
        return client_list

    def get_client(self, client_id: int) -> Client:
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        records = cursor.fetchall()

        client_list = []
        for client in records:
            client = Client(client[0], client[1], client[2], client[3], client[4], client[5], client[6])
            client_list.append(client)
        try:
            return client_list[0]
        except IndexError:
            raise ClientNotFoundError("Error...\nClient does not exist.")

    def remove_client(self, client_id: int) -> bool:
        self.get_client(client_id)  # checks if exists
        sql = """delete from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
        return True

    def update_client(self, client: Client) -> Client:
        self.get_client(client.client_id)  # check if client exists
        sql = """update client set client_firstname=%s, client_lastname=%s, address=%s, city=%s, state=%s, zip_code=%s where client_id=%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client.client_firstname, client.client_lastname, client.address, client.city, client.state,
                             client.zip_code, client.client_id])
        connection.commit()
        return client
