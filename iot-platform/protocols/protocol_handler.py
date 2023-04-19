# from .handler import Handler
# from configs import Config
# from abc import abstractmethod, ABC
# # from utils import Result
#
#
# class ProtocolHandler(Handler):
#
#     def __init__(self, identifier: str, config: Config) -> None:
#         super().__init__(identifier)
#         self._config = config
#
#     @abstractmethod
#     def close(self) -> None:
#         raise NotImplementedError
#
#
# # class ProtocolReadable(ABC):
# #
# #     @abstractmethod
# #     def read(self) -> Result[str]:
# #         raise NotImplementedError