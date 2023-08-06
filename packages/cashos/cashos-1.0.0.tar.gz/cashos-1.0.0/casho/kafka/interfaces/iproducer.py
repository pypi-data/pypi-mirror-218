from abc import ABC, abstractmethod
from .ievent import IEvent
from .imetadata import IMetadata

class IProducer(ABC):
    @abstractmethod
    def send_message(self, metadata: IMetadata, event: IEvent) -> None:
        pass
