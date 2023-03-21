from .action import Action, ActionAgrument
from protocols.handler_all import HandlerAll
from utils import Result
from typing import Any

actions_handler = dict()

def register_handler_action(cls):
    actions_handler[cls().identifier()] = cls
    return cls



@register_handler_action
class ActionHandlerStop(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="stop",
            result_type=Result[bool],
            data_type=bool,
            description="Stops main handler" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop()


@register_handler_action
class ActionHandlerUpdateConfig(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="update_config",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "identifier": ActionAgrument(str, description="Identifier of protocol"),
                "new_conf": ActionAgrument(dict, description="New config (str: Any)")
            },
            description="Update config of given protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.update_config(**kwargs)
    

@register_handler_action
class ActionHandlerProtocolsConfig(Action[Result[dict[str, Any]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocols_config",
            result_type=Result[dict[str, Any]],
            data_type=dict[str, Any],
            description="Config of all avaiblate protocols" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[dict[str, Any]]:
        return handler.protocols_config()
    
@register_handler_action
class ActionHandlerProtocolsInfo(Action[Result[dict[str, Any]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocols_info",
            result_type=Result[dict[str, Any]],
            data_type=dict[str, Any],
            description="Info about all avaiblate protocols" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[dict[str, Any]]:
        return handler.protocols_info()
    
    

@register_handler_action
class ActionHandlerStartProtocols(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocols_start",
            result_type=Result[bool],
            data_type=bool,
            description="Start all protocols" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.start_protocols()
    

@register_handler_action
class ActionHandlerStopProtocols(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocols_stop",
            result_type=Result[bool],
            data_type=bool,
            description="Stop all protocols" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop_protocols()
    

@register_handler_action
class ActionHandlerStopProtocol(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocol_stop",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)")
            },
            description="Stop given protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop_protocol(**kwargs)
    

@register_handler_action
class ActionHandlerStartProtocol(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="protocol_start",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)")
            },
            description="Start given protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.start_protocol(**kwargs)


@register_handler_action
class ActionHandlerApiLayerStart(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layer_start",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "protocol_identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)"),
                "api_identifier": ActionAgrument(arg_type=str, description="Identifier of API layer (name)"),
            },
            description="Start API layer on given protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.start_api_layer(**kwargs)
    

@register_handler_action
class ActionHandlerApiLayerStop(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layer_stop",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "protocol_identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)"),
                "api_identifier": ActionAgrument(arg_type=str, description="Identifier of API layer (name)"),
            },
            description="Stop API layer on given protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop_api_layer(**kwargs)
    
@register_handler_action
class ActionHandlerApiLayersStart(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layers_start",
            result_type=Result[bool],
            data_type=bool,
            description="Start all API layers" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.start_api_layers()
    

@register_handler_action
class ActionHandlerApiLayersStop(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layers_stop",
            result_type=Result[bool],
            data_type=bool,
            description="Stop all API layers" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop_api_layers()
    

@register_handler_action
class ActionHandlerApiLayersProtocolStart(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layers_protocol_start",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "protocol_identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)"),
            },
            description="Start all API layers on protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.start_protocol_api_layers(**kwargs)
    

@register_handler_action
class ActionHandlerApiLayersProtocolStop(Action[Result[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="api_layers_protocol_stop",
            result_type=Result[bool],
            data_type=bool,
            allowed_args={
                "protocol_identifier": ActionAgrument(arg_type=str, description="Identifier of protocol (name)"),
            },
            description="Stop all API layers on protocol" 
        )

    def _action(self, handler: HandlerAll, **kwargs) -> Result[bool]:
        return handler.stop_protocol_api_layers(**kwargs)