from dataclasses import dataclass
from typing import Generic, TypeVar, Any
from enum import Enum
import json


T = TypeVar('T')

class Protocol(Enum):
    WIRE_1 = "1-Wire"
    BLUETOOTH = "Bluetooth"
    NB_IOT = "NB-IoT"
    DMX = "DMX"
    RS_232 = "RS-232"
    MAX30102 = "MAX30102"
    NEO = "NEO"


@dataclass
class Result(Generic[T]):
    data: T
    passed: bool = False
    message: str = ""
    error: str = ""
    protocol: Protocol = None

    def to_dict(self) -> dict[str, Any]:
        temp = dict()
        if self.protocol:
            temp["protocol"] = self.protocol.value
        temp["passed"] = self.passed
        #if self.data:
        temp["data"] = self.data
        temp["message"] = self.message
        if self.error:
            temp["error"] = str(self.error)

        return temp

    def json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class Result1Wire(Result, Generic[T]):
    protocol: Protocol = Protocol.WIRE_1

    def __post__init__(self, config: dict):
        self.__init__(**config)

@dataclass
class ResultBluetooth(Result, Generic[T]):
    protocol: Protocol = Protocol.BLUETOOTH

    def __post__init__(self, config: dict):
        self.__init__(**config)

@dataclass
class ResultNBIoT(Result, Generic[T]):
    protocol: Protocol = Protocol.NB_IOT

    def __post__init__(self, config: dict):
        self.__init__(**config)


@dataclass
class ResultDMX(Result, Generic[T]):
    protocol: Protocol = Protocol.DMX

    def __post__init__(self, config: dict):
        self.__init__(**config)


@dataclass
class ResultMAX30102(Result, Generic[T]):
    protocol: Protocol = Protocol.MAX30102

    def __post__init__(self, config: dict):
        self.__init__(**config)

@dataclass
class ResultNEO(Result, Generic[T]):
    protocol: Protocol = Protocol.NEO

    def __post__init__(self, config: dict):
        self.__init__(**config)
    
