from abc import ABC, abstractmethod
from typing import List
from ..models.producer import Producer


class ProducerRepository(ABC):
    @abstractmethod
    def save(self, producer: Producer) -> Producer:
        pass

    @abstractmethod
    def get_min_intervals(self):
        pass

    @abstractmethod
    def get_max_intervals(self):
        pass
