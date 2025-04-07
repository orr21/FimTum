from abc import ABC, abstractmethod

class Crawler(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass