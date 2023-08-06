from abc import ABC, abstractmethod
from typing import Callable
from .ievent import IEvent

class IConsumer(ABC):
    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[IEvent], None]) -> None:
        pass
