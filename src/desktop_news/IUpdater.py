from abc import ABC, abstractmethod


class IUpdater(ABC):

    @abstractmethod
    def update(self) -> str:
        pass
