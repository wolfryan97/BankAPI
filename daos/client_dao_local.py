from typing import List
from daos.client_dao import ClientDao
from entities.client import Client
from exceptions.client_not_found import ClientNotFoundError


class ClientDaoLocal(ClientDao):
    client_table = {}
    id_maker = 0

    def create_client(self, client: Client) -> Client:
        ClientDaoLocal.id_maker += 1
        client.client_id = ClientDaoLocal.id_maker
        ClientDaoLocal.client_table[client.client_id] = client
        return client

    def get_all_clients(self) -> List[Client]:
        return list(self.client_table)

    def get_client(self, client_id: int) -> Client:
        try:
            return ClientDaoLocal.client_table[client_id]
        except KeyError:
            raise ClientNotFoundError("An error occurred.\nPlease enter valid client information.")

    def remove_client(self, client_id: int) -> bool:
        try:
            self.client_table.pop(client_id)
            return True
        except KeyError:
            raise ClientNotFoundError("An error occurred.\nPlease enter valid client information.")

    def update_client(self, client: Client) -> Client:
        try:
            c: Client = self.client_table[client.client_id]
            c.address = client.address
            c.city = client.city
            c.state = client.state
            c.zip_code = client.zip_code
            return client
        except KeyError:
            raise ClientNotFoundError("An error occurred.\nPlease enter valid account information.")
