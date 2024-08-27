from abc import ABC, abstractmethod


class ModelRegistry(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self):
        pass
