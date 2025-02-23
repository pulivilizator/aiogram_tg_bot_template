from abc import ABC, abstractmethod

class BaseInteractor(ABC):
    @abstractmethod
    async def execute(self, *args):
        raise NotImplementedError
