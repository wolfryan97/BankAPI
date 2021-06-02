from typing import List

from daos.client_dao import ClientDao
from entities.client import Client
from services.client_service import ClientService


class ClientServiceImpl(ClientService):

    def __init__(self, client_dao: ClientDao):
        self.client_dao = client_dao

    def create_client(self, client: Client) -> Client:
        return self.client_dao.create_client(client)

    def get_all_clients(self) -> List[Client]:
        return self.client_dao.get_all_clients()

    def get_client(self, client_id: int) -> Client:
        return self.client_dao.get_client(client_id)

    def remove_client(self, client_id: int) -> Client:
        return self.client_dao.remove_client(client_id)

    def update_client(self, client: Client) -> Client:
        return self.client_dao.update_client(client)

    # Unused
    def get_client_by_name(self, phrase: str) -> List[Client]:
        li = self.get_all_clients()
        results = []
        for client in li:
            if phrase.strip() == client.client_firstname.strip() or \
                    phrase.strip() == client.client_lastname.strip():
                results.append(client)
        return results
