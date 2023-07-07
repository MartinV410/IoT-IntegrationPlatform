from .action import Action, ActionAgrument
from protocols.protocol_handler_neo_m8m import ProtocolHandlerNEO
from utils import ResultNEO

actions_neo = dict()

def register_neo_action(cls):
    actions_neo[cls().identifier()] = cls
    return cls


@register_neo_action
class ActionNEOPosition(Action[ResultNEO[dict]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="get_position",
            result_type=ResultNEO[dict],
            data_type=dict,
            description="Get position" 
        )

    def _action(self, handler: ProtocolHandlerNEO, **kwargs) -> ResultNEO[dict]:
        return handler.position(**kwargs)
    