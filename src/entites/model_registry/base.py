from abc import ABC, abstractmethod


class ModelRegistry(ABC):

    @abstractmethod
    def predict(self):
        pass
