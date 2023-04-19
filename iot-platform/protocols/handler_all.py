# HANDLERS
from .handler import Handler
#from .protocol_handler import ProtocolHandler
from .protocol_handler_1wire import ProtocolHandler1Wire
from .protocol_handler_bluetooth import ProtocolHandlerBluetooth
from .protocol_handler_nbiot import ProtocolHandlerNBIoT
from .protocol_handler_dmx import ProtocolHandlerDMX
# ACTIONS
from actions.actions_1wire import actions_1wire
from actions.actions_bluetooth import actions_bluetooth
from actions.actions_nbiot import actions_nbiot
from actions.actions_dmx import actions_dmx
# RESULTS
from utils import Result1Wire, ResultBluetooth, ResultNBIoT,ResultDMX, Result
# CONFIGS
from configs import Config1Wire, ConfigBluetooth, ConfigNBIoT, ConfigDMX, Config, ConfigControl
# MANAGERS
from managers.manager_config import ManagerConfig
from managers.manager_handler import ManagerHandler
from managers.manager_actions import ManagerActions
from managers.manager_zmq_rep import ManagerZmqRep
# API LAYERS
from api.api_layer_ws import ApiLayerWs
from api.api_layer import ApiLayer
# UTILS
from utils import Protocol
# BUILTINS
from copy import deepcopy
from multiprocessing import Event
import logging
from typing import Any, Dict, List
from dataclasses import dataclass, field
import datetime, time

DEFAULT_PORT = 50000


@dataclass
class ApiLayerWrapper:
    identifier: str
    stop_event: Event
    api_layer: ApiLayer
    api_layer_class: ApiLayer
    running: bool = False


@dataclass
class HandlerWrapper:
    identifier: str
    handler_class: Handler
    actions: dict
    result_class: Result
    config_class: Config
    api_layers_classes: List = field(default_factory=lambda: [])

    # THOSE ARE ADDED AT RUNTIME!
    manager: ManagerHandler = None
    stop_event: Event = None
    running: bool = False
    start_date: datetime.datetime = datetime.datetime.now()
    config: Config = None
    api_layers: List[ApiLayerWrapper] = field(default_factory=lambda: [])

    def info_api_layers(self) -> Dict:
        info = dict()
        for layer in self.api_layers:
            info[layer.identifier] = layer.api_layer.info()

        return info

    def info(self) -> Dict:
        temp = dict()
        temp["running"] = self.running
        if self.running: temp["start_date"] = self.start_date
        temp["actions"] = len(self.actions)
        temp["api_layers"] = self.info_api_layers()
        temp["config"] = self.config.__dict__

        data = dict()
        data[self.identifier] = temp
        return data


class HandlerAll:
    def __init__(self) -> None:
        self.__manager_config = ManagerConfig("config.ini")

        from actions.actions_handler_all import actions_handler  # To prevent circular import
        self.__manager_actions = ManagerActions(actions_handler, Result)

        self.__running = False

        # NEW PROTOCOLS MUST BE ADDED HERE TO BE PART OF THE PLATFORM
        self.__protocols = [
            HandlerWrapper(
                identifier=Protocol.WIRE_1.value,
                handler_class=ProtocolHandler1Wire,
                actions=actions_1wire,
                result_class=Result1Wire,
                config_class=Config1Wire
            ),
            HandlerWrapper(
                identifier=Protocol.BLUETOOTH.value,
                handler_class=ProtocolHandlerBluetooth,
                actions=actions_bluetooth,
                result_class=ResultBluetooth,
                config_class=ConfigBluetooth,
                api_layers_classes=[ApiLayerWs]
            ),
            HandlerWrapper(
                identifier=Protocol.NB_IOT.value,
                handler_class=ProtocolHandlerNBIoT,
                actions=actions_nbiot,
                result_class=ResultNBIoT,
                config_class=ConfigNBIoT,
            ),
            HandlerWrapper(
                identifier=Protocol.DMX.value,
                handler_class=ProtocolHandlerDMX,
                actions=actions_dmx,
                result_class=ResultDMX,
                config_class=ConfigDMX
            ),
        ]

    def __prepare_api_layers(self) -> None:
        # Configs must be added in protocol wrappers before calling this!! 
        for wrapper in self.__protocols:
            for api_layer_class in wrapper.api_layers_classes:
                stop_event = Event()

                api_layer = api_layer_class(stop_event=stop_event, config=wrapper.config)
                api_wrapper = ApiLayerWrapper(api_layer.identifier(), stop_event, api_layer, api_layer_class)
                wrapper.api_layers.append(api_wrapper)

    def start_api_layer(self, protocol_identifier: str, api_identifier: str, startup: bool = False) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == protocol_identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{protocol_identifier}' not found!")
        
        api_layer = next((item for item in protocol.api_layers if item.identifier == api_identifier), None)
        if not api_layer:
            return Result[bool](data=False, message=f"Api layer '{api_identifier}' not found in protocol '{protocol_identifier}'!")

        if api_layer.api_layer.is_alive():
            return Result[bool](data=False, message=f"Api layer '{api_identifier}' is already running!")
        
        if api_layer.stop_event.is_set():  # reset stop event if necessary
            api_layer.stop_event.clear()

        if startup:
            if not protocol.config.autostart:
                return Result[bool](data=False, message=f"Not starting api layer '{api_identifier}' because protocol autostart is false!")
            if not api_layer.api_layer.autostart():
                return Result[bool](data=False, message=f"Not starting api layer '{api_identifier}' because autostart is false!")
        
        logging.info(f"Starting API layer '{api_identifier}' for '{protocol_identifier}'")
        api_layer.api_layer = api_layer.api_layer_class(stop_event=api_layer.stop_event, config=protocol.config)
        api_layer.api_layer.start()
        logging.info(f"API layer '{api_identifier}' for '{protocol_identifier}' started")
        return Result[bool](passed=True, data=True, message=f"Api layer '{api_identifier}' in protocol '{protocol_identifier}' started")

    def stop_api_layer(self, protocol_identifier: str, api_identifier: str) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == protocol_identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{protocol_identifier}' not found!")
        
        api_layer = next((item for item in protocol.api_layers if item.identifier == api_identifier), None)
        if not api_layer:
            return Result[bool](data=False, message=f"Api layer '{api_identifier}' not found in protocol '{protocol_identifier}'!")
        
        if not api_layer.api_layer.is_alive():
            return Result[bool](data=False, message=f"Api layer '{api_identifier}' is already stopped!")
        
        logging.info(f"Stopping API layer '{api_identifier}' for '{protocol_identifier}'")
        api_layer.stop_event.set()
        api_layer.api_layer.kill()  # TODO zmenit ked bude async break loop dorobena v ApiLayerWebsocket
        logging.info(f"API layer '{api_identifier}' for '{protocol_identifier}' stopped")
        return Result[bool](passed=True, data=True, message=f"Api layer '{api_identifier}' in protocol '{protocol_identifier}' stopped")

    def start_api_layers(self, startup: bool = False) -> Result[bool]:
        for wrapper in self.__protocols:
            for api_layer in wrapper.api_layers:
                self.start_api_layer(wrapper.identifier, api_layer.identifier, startup)

        return Result[bool](passed=True, data=True, message="All API layers started")
    
    def stop_api_layers(self) -> Result[bool]:
        for wrapper in self.__protocols:
            for api_layer in wrapper.api_layers:
                self.stop_api_layer(wrapper.identifier, api_layer.identifier)

        return Result[bool](passed=True, data=True, message="All API layers stopped ")
    
    def start_protocol_api_layers(self, protocol_identifier: str, startup: bool = False) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == protocol_identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{protocol_identifier}' not found!")
        
        for api_layer in protocol.api_layers:
            self.start_api_layer(protocol_identifier, api_layer.identifier, startup)
        
        return Result[bool](passed=True, data=True, message=f"All API layers were started for protocol '{protocol_identifier}'")
    
    def stop_protocol_api_layers(self, protocol_identifier: str) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == protocol_identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{protocol_identifier}' not found!")
        
        for api_layer in protocol.api_layers:
            self.stop_api_layer(protocol_identifier, api_layer.identifier)
        
        return Result[bool](passed=True, data=True, message=f"All API layers were stopped for protocol '{protocol_identifier}'")

    def start_protocols(self, startup: bool = False) -> Result[bool]:
        started = 0
        for protocol in self.__protocols:
            start = self.start_protocol(protocol.identifier, startup=startup)
            if start.passed:
                started += 1

        return Result[bool](passed=True, data=True, message=f"Started {started} protocols ({len(self.__protocols) - started} already running)")

    def stop_protocols(self) -> Result[bool]:
        stopped = 0
        for protocol in self.__protocols:
            start = self.stop_protocol(protocol.identifier)
            if start.passed:
                stopped += 1

        return Result[bool](passed=True, data=True, message=f"Stopped {stopped} protocols ({len(self.__protocols) - stopped} were already off)")

    def start_protocol(self, identifier: str, startup: bool = False) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{identifier}' not found!")
        
        if protocol.running:
            return Result[bool](data=False, message=f"Protocol '{identifier}' is allready running!")

        config = self.__manager_config.get_config(protocol.config_class, identifier)
        
        if not config.passed:
            return Result[bool](data=False, message=config.message, error=config.error)
        
        new_stop_event = Event()
        new_manager = ManagerHandler[protocol.handler_class, protocol.result_class](handler=protocol.handler_class, actions=protocol.actions, config=config.data, stop_event=new_stop_event, result_type=protocol.result_class, identifier=identifier)

        protocol.stop_event = new_stop_event
        protocol.manager = new_manager
        protocol.config = config.data

        if startup and not config.data.autostart:  # if autostart is disabled for ptorocol
            return Result[bool](data=False, message=f"Not starting protocol '{identifier}' because autostart is disabled")
        else:
            protocol.running = True
            new_manager.start()
            self.start_protocol_api_layers(identifier, startup)
            return Result[bool](passed=True, data=True, message=f"Protocol '{identifier}' started successfuly")

    def stop_protocol(self, identifier: str) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with identifier '{identifier}' not found!")
        
        if not protocol.running:
            return Result[bool](data=False, message=f"Protocol with identifier '{identifier}' is not running!")

        if protocol.running:
            protocol.stop_event.set()
            protocol.manager.join()
            protocol.running = False
            self.stop_protocol_api_layers(identifier)
        return Result[bool](passed=True, data=True, message="Protocol stopped")

    def start(self) -> None:
        logging.info("Main handler started")

        # START PROTOCOLS MANAGERS
        conf_r = self.__manager_config.read()
        zmq_rep = ManagerZmqRep
        if conf_r.passed:
            config = self.__manager_config.get_config(ConfigControl, "Control").data
            logging.info(f"Main handler using port {config.zmq_port} for control")
            zmq_rep = ManagerZmqRep(config.zmq_port, Result)

            self.start_protocols(startup=True)  # start all protocols (if autostart is on)
            self.__prepare_api_layers()  # prepare api layers before running them
            self.start_api_layers(startup=True)
        else:
            logging.critical(conf_r.message)
            zmq_rep = ManagerZmqRep(DEFAULT_PORT, Result)
            logging.info(f"Main handler using default port {DEFAULT_PORT} for control")

        self.__running = True
        while self.__running:
            message_r = zmq_rep.receive()

            # CHECK IF MESSAGE WAS RECEIVED
            if not message_r.passed:  
                if not message_r.error:  # if timeout occured
                    continue
                # when message is not json serializable or another unexpected error occured
                zmq_rep.respond([message_r])
                continue

            actions_r = self.__manager_actions.manage_actions(message_r.data, self)
            zmq_rep.respond(actions_r)

        # CLEANUP
        logging.info("Stopping main handler")
        zmq_rep.close()
        self.stop_api_layers()
        self.stop_protocols()
        logging.info("Main handler stopped")

    def stop(self) -> Result[bool]:
        self.__running = False
        return Result[bool](passed=True, data=True, message="Stop issued for main handler")

    def update_config(self, identifier: str, new_conf: Dict[str, Any]) -> Result[bool]:
        protocol = next((item for item in self.__protocols if item.identifier == identifier), None)
        if not protocol:
            return Result[bool](data=False, message=f"Protocol with given identifier '{identifier}' not found!")
        
        update_r = self.__manager_config.update(protocol.config_class, identifier, new_conf)
        if not update_r.passed:
            return update_r
        
        was_running = protocol.running

        self.stop_protocol(identifier)

        if was_running:
            self.start_protocol(identifier)

        return Result[bool](passed=True, data=True, message=f"Protocol '{identifier}' configuration updated")

    def protocols_config(self) -> Result[Dict[str, Any]]:
        info = dict()

        for protocol in self.__protocols:
            config = self.__manager_config.get_config(protocol.config_class, protocol.identifier)
            if config.passed:
                info[protocol.identifier] = config.data.__dict__

        return Result[Dict[str, Any]](passed=True, data=info, message="Protocols configurations")
    
    def protocols_info(self) -> Result[Dict[str, Any]]:
        info = dict()

        for protocol in self.__protocols:
            info.update(protocol.info())

        return Result[Dict[str, Any]](passed=True, data=info, message="Protocols Information")

        
