from dataclasses import dataclass

@dataclass
class ConfigControl:
    zmq_port: int

@dataclass
class Config:
    autostart: bool
    zmq_port: int

@dataclass
class ConfigWebsocket:
    websocket_autostart: bool
    websocket_port: int # websocket port
    zmq_port_pub: int # port of local zmq publisher

@dataclass
class ConfigPublish:
    zmq_port_pub: int


@dataclass 
class Config1Wire(Config):
    pass


@dataclass
class ConfigBluetooth(Config, ConfigWebsocket, ConfigPublish):
    serial_port: str


@dataclass
class ConfigNBIoT(Config):
    serial_port: str
    serial_baud: int
    serial_timeout: float


@dataclass
class ConfigDMX(Config):
    serial_port: str

@dataclass
class ConfigMAX30102(Config):
    address: int
    channel: int
    gpio_pin: int

@dataclass
class ConfigNEO(Config):
    serial_port: str

