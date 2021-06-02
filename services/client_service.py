from abc import ABC, abstractmethod
from typing import List
from entities.client import Client


class ClientService(ABC):
    @abstractmethod
    def create_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def remove_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def update_client(self, client: Client) -> Client:
        pass

    @abstractmethod
    def get_client_by_name(self, phrase: str) -> List[Client]:
        pass
