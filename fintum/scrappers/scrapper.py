from abc import ABC, abstractmethod

class Scrapper(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass