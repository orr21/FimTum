from abc import ABC, abstractmethod
from typing import Set

class UrlBuilder(ABC):

    def __init__(self, base_url: str):
        self.url = base_url
        self._valid_urls = self.select_valid_urls()

    @abstractmethod
    def get_url(self, month: int, year: int) -> str:
        pass

    @abstractmethod
    def select_valid_urls(self) -> Set[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_links(html: str) -> Set[str]:
        pass