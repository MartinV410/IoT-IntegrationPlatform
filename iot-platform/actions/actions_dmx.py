from .action import Action, ActionAgrument
from protocols.protocol_handler_dmx import ProtocolHandlerDMX
from utils import ResultDMX
from PyDMXControl.profiles.Generic import RGB_Vdim
from PyDMXControl.profiles.defaults import Fixture
from typing import List, Dict

actions_dmx = dict()

def register_dmx_action(cls):
    actions_dmx[cls().identifier()] = cls
    return cls


@register_dmx_action
class ActionDMXAddFixture(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="add_fixture",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture": ActionAgrument(arg_type=str, description="Fixture type", options=["RGB"]),
                "name": ActionAgrument(arg_type=str, optional=True, description="Fixture name"),
                "channel": ActionAgrument(arg_type=int, optional=True, description="Fixture starting channel"),
            },
            description="Add fixture to universe" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        fixture = Fixture
        if kwargs["fixture"] == "RGB":
            fixture = RGB_Vdim

        kwargs["fixture"] = fixture
        return handler.add_fixture(**kwargs)
    

@register_dmx_action
class ActionDMXAllLocate(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_locate",
            result_type=ResultDMX[bool],
            data_type=bool,
            description="Locate all available fixtures" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.all_locate()
    

@register_dmx_action
class ActionDMXAllFixtures(Action[ResultDMX[List[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_fixtures",
            result_type=ResultDMX[List[dict]],
            data_type=List[dict],
            description="Informations about all available fixtures" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[List[dict]]:
        return handler.all_fixtures()
    

@register_dmx_action
class ActionDMXAllOn(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_on",
            result_type=ResultDMX[bool],
            data_type=bool,
            description="Turns on all available fixtures" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.all_on()
    
@register_dmx_action
class ActionDMXAllOff(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_off",
            result_type=ResultDMX[bool],
            data_type=bool,
            description="Turns off all available fixtures" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.all_off()
    

@register_dmx_action
class ActionDMXAllColor(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_color",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "red": ActionAgrument(arg_type=int, description="Red color value in range 0-255"),
                "green": ActionAgrument(arg_type=int, description="Green color value in range 0-255"),
                "blue": ActionAgrument(arg_type=int, description="Blue color value in range 0-255"),
            },
            description="Set color for all available fixtures that supports color changing" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.all_color(**kwargs)
    

@register_dmx_action
class ActionDMXAllDim(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_dim",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "value": ActionAgrument(arg_type=int, description="Dim value in range 0-255"),
            },
            description="Dim all available fixtures that supports that" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.all_dim(**kwargs)
    

@register_dmx_action
class ActionDMXAllDelete(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="all_delete",
            result_type=ResultDMX[bool],
            data_type=bool,
            description="Delete all fixtures" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.delete_all()
    

@register_dmx_action
class ActionDMXDeleteFixture(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_delete",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Delete fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.delete_fixture(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureLocate(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_locate",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Locate fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.fixture_locate(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureoOn(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_on",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Turn on fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.fixture_on(**kwargs)


@register_dmx_action
class ActionDMXFixtureOff(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_off",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Turn off fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.fixture_off(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureDim(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_dim",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
                "value": ActionAgrument(arg_type=int, description="Dim value in range 0-255"),
            },
            description="Dim fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.fixture_dim(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureColorSet(Action[ResultDMX[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_color_set",
            result_type=ResultDMX[bool],
            data_type=bool,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
                "red": ActionAgrument(arg_type=int, description="Red color value in range 0-255"),
                "green": ActionAgrument(arg_type=int, description="Green color value in range 0-255"),
                "blue": ActionAgrument(arg_type=int, description="Blue color value in range 0-255"),
            },
            description="Set colors of fixture with given ID if its supported" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[bool]:
        return handler.fixture_color_set(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureColorGet(Action[ResultDMX[List[int]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_color_get",
            result_type=ResultDMX[List[int]],
            data_type=List[int],
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Get current colors of fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[List[int]]:
        return handler.fixture_color_get(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureChannels(Action[ResultDMX[Dict[int, Dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_channels",
            result_type=ResultDMX[Dict[int, Dict]],
            data_type=Dict[int, Dict],
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Get occupied channels of fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[Dict[int, Dict]]:
        return handler.fixture_channels(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureChannelUsage(Action[ResultDMX[Dict[str, int]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_channel_usage",
            result_type=ResultDMX[Dict[str, int]],
            data_type=Dict[str, int],
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Get channel usage of fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[Dict[str, int]]:
        return handler.fixture_channel_usage(**kwargs)
    

@register_dmx_action
class ActionDMXFixtureInfo(Action[ResultDMX[Dict]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="fixture_info",
            result_type=ResultDMX[Dict],
            data_type=Dict,
            allowed_args={
                "fixture_id": ActionAgrument(arg_type=int, description="ID of fixture"),
            },
            description="Get info about fixture with given ID" 
        )

    def _action(self, handler: ProtocolHandlerDMX, **kwargs) -> ResultDMX[Dict]:
        return handler.fixture_info(**kwargs)