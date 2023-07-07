from .action import Action, ActionAgrument
from protocols.protocol_handler_max30102 import ProtocolHandlerMAX30102
from utils import ResultMAX30102
from typing import List, Dict

actions_max30102 = dict()

def register_max30102_action(cls):
    actions_max30102[cls().identifier()] = cls
    return cls


@register_max30102_action
class ActionMAX30102FiFo(Action[ResultMAX30102[dict]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="read_fifo",
            result_type=ResultMAX30102[dict],
            data_type=dict,
            description="Get FIFO values" 
        )

    def _action(self, handler: ProtocolHandlerMAX30102, **kwargs) -> ResultMAX30102[dict]:
        return handler.read_fifo(**kwargs)
    

@register_max30102_action
class ActionMAX30102Sequential(Action[ResultMAX30102[dict]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="read_sequential",
            result_type=ResultMAX30102[dict],
            data_type=dict,
            allowed_args={
                "amount": ActionAgrument(arg_type=int, optional=True, description="Read amount of times")
            },
            description="Read values x times" 
        )

    def _action(self, handler: ProtocolHandlerMAX30102, **kwargs) -> ResultMAX30102[dict]:
        return handler.read_sequential(**kwargs)