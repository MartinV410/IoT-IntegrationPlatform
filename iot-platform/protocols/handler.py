from abc import abstractmethod, ABC

class Handler(ABC):
    
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier

    def identifier(self) -> str:
        return self._identifier

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError