from .action import Action, ActionAgrument
from protocols.protocol_handler_bluetooth import ProtocolHandlerBluetooth, Switchable
from utils import ResultBluetooth

actions_bluetooth = dict()

def register_bl_action(cls):
    actions_bluetooth[cls().identifier()] = cls
    return cls



@register_bl_action
class ActionBluetoothDeviceServices(Action[ResultBluetooth[list[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="services",
            result_type=ResultBluetooth[list[dict]],
            data_type=list[dict],
            allowed_args={
                "addr": ActionAgrument(arg_type=str, description="Mac address of device")
            },
            description="Get bluetooth services of given device" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[list[dict]]:
        return handler.services(**kwargs)


@register_bl_action
class ActionBluetoothDiscoverDevices(Action[ResultBluetooth[list[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="discover",
            result_type=ResultBluetooth[list[dict]],
            data_type=list[dict],
            allowed_args={
                "duration": ActionAgrument(arg_type=int, description="Duration of discovery in seconds"),
                "lookup_names": ActionAgrument(arg_type=bool, optional=True, description="If names should be included during discovery"),
                "lookup_class": ActionAgrument(arg_type=bool, optional=True, description="If class should be included during discovery")
            },
            description="Discover all available devices" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[list[dict]]:
        return handler.discover_devices(**kwargs)


@register_bl_action
class ActionBluetoothLocalAddr(Action[ResultBluetooth[str]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="local_addr",
            result_type=ResultBluetooth[str],
            data_type=str,
            description="Get local mac address" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[str]:
        return handler.local_addr()


@register_bl_action
class ActionBluetoothSetAlias(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_alias",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "new_alias": ActionAgrument(arg_type=str, description="New device alias")
            },
            description="Set new alias" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[str]:
        return handler.set_alias(**kwargs)


@register_bl_action
class ActionBluetoothPairedDevices(Action[ResultBluetooth[list[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="paired_devices",
            result_type=ResultBluetooth[list[dict]],
            data_type=list[dict],
            description="Get all paired devices" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[list[dict]]:
        return handler.paired_devices()


@register_bl_action
class ActionBluetoothSwitchPower(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="switch_power",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "on": ActionAgrument(arg_type=bool, description="On/Off")
            },
            description="Switch power of bluetooth" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.switch_function(Switchable.POWER, **kwargs)


@register_bl_action
class ActionBluetoothSwitchPairable(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="switch_pairable",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "on": ActionAgrument(arg_type=bool, description="On/Off")
            },
            description="Switch if device is pairable" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.switch_function(Switchable.PAIRABLE, **kwargs)


@register_bl_action
class ActionBluetoothSwitchDiscoverable(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="switch_discoverable",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "on": ActionAgrument(arg_type=bool, description="On/Off")
            },
            description="Switch if device is discoverable" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.switch_function(Switchable.DISCOVERABLE, **kwargs)


@register_bl_action
class ActionBluetoothIsOn(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="is_on",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            description="Check if bluetooth is on" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.is_on()


@register_bl_action
class ActionBluetoothIsDiscoverable(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="is_discoverable",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            description="Check if device is discoverable" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.is_discoverable()


@register_bl_action
class ActionBluetoothIsPairable(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="is_pairable",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            description="Check if device is pairable" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.is_pairable()


@register_bl_action
class ActionBluetoothUnpair(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="unpair",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "addr": ActionAgrument(arg_type=str, description="Mac address of device")
            },
            description="Unpair device with given mac address" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.unpair(**kwargs)


@register_bl_action
class ActionBluetoothPair(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="pair",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "addr": ActionAgrument(arg_type=str, description="Mac address of device")
            },
            description="Pair with device" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[bool]:
        return handler.pair(**kwargs)


@register_bl_action
class ActionBluetoothWrite(Action[ResultBluetooth[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="write",
            result_type=ResultBluetooth[bool],
            data_type=bool,
            allowed_args={
                "message": ActionAgrument(arg_type=str, description="Message")
            },
            description="Write to bluetooth buffer" 
        )

    def _action(self, handler: ProtocolHandlerBluetooth, **kwargs) -> ResultBluetooth[str]:
        return handler.write(**kwargs)