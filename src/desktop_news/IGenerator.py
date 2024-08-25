from abc import ABC, abstractmethod


class IGenerator(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> dict:
        pass
