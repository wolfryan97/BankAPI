from abc import ABC, abstractmethod
from typing import List
from entities.client import Client


# Data Access Object
class ClientDao(ABC):

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
