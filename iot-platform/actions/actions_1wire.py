from .action import Action, ActionAgrument
from protocols.protocol_handler_1wire import ProtocolHandler1Wire
from utils import Result1Wire
from pi1wire import Resolution

actions_1wire = dict()

def register_1wire_action(cls):
    actions_1wire[cls().identifier()] = cls
    return cls


@register_1wire_action
class Action1WireFindAvailable(Action[Result1Wire[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="find_available",
            result_type=Result1Wire[bool],
            data_type=bool,
            description="Find available 1-Wire devices" 
        )

    def _action(self, handler: ProtocolHandler1Wire, **kwargs) -> Result1Wire[list[dict]]:
        return handler.find_available()


@register_1wire_action
class Action1WireTemperature(Action[Result1Wire[float]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="get_temperature",
            result_type=Result1Wire[float],
            data_type=float,
            allowed_args={
                "sensor_mac": ActionAgrument(arg_type=str, description="MAC address of sensor")
            },
            description="Get temperature of given device" 
        )

    def _action(self, handler: ProtocolHandler1Wire, **kwargs) -> Result1Wire[float]:
        return handler.get_temperature(**kwargs)


@register_1wire_action
class Action1WireTemperatures(Action[Result1Wire[list[dict[str, float]]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="get_temperatures",
            result_type=Result1Wire[list[dict[str, float]]],
            data_type=list[dict[str, float]],
            description="Get temperatures of all available devices",
        )

    def _action(self, handler: ProtocolHandler1Wire, **kwargs) -> Result1Wire[list[dict[str, float]]]:
        return handler.get_temperatures()


@register_1wire_action
class Action1WireChangeResolution(Action[Result1Wire[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="change_resolution",
            result_type=Result1Wire[bool],
            data_type=bool,
            allowed_args={
                "sensor_mac": ActionAgrument(arg_type=str, description="Sensor MAC address"),
                "resolution": ActionAgrument(arg_type=int, description="Resolution", options=[9, 10, 11, 12])
            },
            description="Change sensing resolution of device" 
        )

    def _action(self, handler: ProtocolHandler1Wire, **kwargs) -> Result1Wire[bool]:
        return handler.change_resolution(kwargs["sensor_mac"], Resolution(kwargs["resolution"]))


@register_1wire_action
class Action1WireChangeResolutionAll(Action[Result1Wire[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="change_resolution_all",
            result_type=Result1Wire[bool],
            data_type=bool,
            allowed_args={
                "resolution": ActionAgrument(arg_type=int, description="Resolution", options=[9, 10, 11, 12])
            },
            description="Change sensing resolution of device" 
        )

    def _action(self, handler: ProtocolHandler1Wire, **kwargs) -> Result1Wire[bool]:
        return handler.change_resolution_all(Resolution(kwargs["resolution"]))