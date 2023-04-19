from abc import abstractmethod, ABC
from utils import Result
from configs import Config


class Handler(ABC):
    
    def __init__(self, identifier: str, config: Config) -> None:
        self._identifier = identifier
        self._config = config

    def identifier(self) -> str:
        return self._identifier

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class HandlerReadable(ABC):

    @abstractmethod
    def read(self) -> Result[str]:
        raise NotImplementedError