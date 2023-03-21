from .action import Action, ActionAgrument
from protocols.protocol_handler_nbiot import ProtocolHandlerNBIoT
from utils import ResultNBIoT

actions_nbiot = dict()

def register_nbiot_action(cls):
    actions_nbiot[cls().identifier()] = cls
    return cls


@register_nbiot_action
class ActionNBIoTPrefferedCelularModes(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="preffered_celular_modes",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get preffered celular modes (CNMP=?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.preffered_celular_modes()


@register_nbiot_action
class ActionNBIoTPrefferedCelularModeCurrent(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="preffered_celular_mode_current",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current preffered celular mode (CNMP?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.preffered_celular_mode_current()


@register_nbiot_action
class ActionNBIoTSetPrefferedCelularMode(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_preffered_celular_mode",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "mode": ActionAgrument(arg_type=int, description="Preffered celular mode")
            },
            description="Set preffered celular mode (CNMP=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.set_preffered_celular_mode(**kwargs)


@register_nbiot_action
class ActionNBIoTPrefferedCelularProtocolModes(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="preffered_celular_protocol_modes",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get preffered celular protocol modes (CNMB=?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.preffered_celular_protocol_modes()


@register_nbiot_action
class ActionNBIoTPrefferedCelularProtocolModeCurrent(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="preffered_celular_protocol_mode_current",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current preffered celular protocol mode (CNMB?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.preffered_celular_protocol_mode_current()


@register_nbiot_action
class ActionNBIoTSetPrefferedCelularProtocolMode(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_preffered_celular_protocol_mode",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "mode": ActionAgrument(arg_type=int, description="Protocol mode")
            },
            description="Get current preffered celular protocol mode (CNMB=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_preffered_celular_protocol_mode(**kwargs)


@register_nbiot_action
class ActionNBIoTInquiringUEInfo(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="inquiring_ue_info",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get inquiring UE system information (CPSI?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.inquiring_ue_sysinfo()


@register_nbiot_action
class ActionNBIoTNetworkRegistration(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="network_registration",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get all available network providers (GREG?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.network_registration()


@register_nbiot_action
class ActionNBIoTSetNetworkRegistration(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_network_registration",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "mode": ActionAgrument(arg_type=int, description="Registration mode")
            },
            description="Set network registration mode (GREG=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_network_registration(**kwargs)


@register_nbiot_action
class ActionNBIoTPhoneFunctionalityCurrent(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="phone_functionality_current",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current phone functionality (CFUN?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.phone_functionality_current()


@register_nbiot_action
class ActionNBIoTSetPhoneFunctionality(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_phone_functionality",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "mode": ActionAgrument(arg_type=str, description="phone functionality mode")
            },
            description="Set phone functionality (CFUN=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.phone_functionality(**kwargs)


@register_nbiot_action
class ActionNBIoTSignalQuality(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="signal_quality",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current signal quality (CSQ)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.signal_quality()


@register_nbiot_action
class ActionNBIoTOperatorsAvailable(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="operators_available",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current available operators (COPS=?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.operators_available()


@register_nbiot_action
class ActionNBIoTOperatorMode(Action[ResultNBIoT[list[str]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="operator_mode",
            result_type=ResultNBIoT[list[str]],
            data_type=list[str],
            description="Get current operator mode (COPS?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[str]]:
        return handler.operator_mode()


@register_nbiot_action
class ActionNBIoTSetOperator(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_operator_mode",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "mode": ActionAgrument(arg_type=str, description="Operator mode")
            },
            description="Set operator mode (COPS=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_operator(**kwargs)


@register_nbiot_action
class ActionNBIoTSetErrorsNumeric(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_errors_numeric",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            description="Set errors to be displayed in numeric mode (CMEE=1)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_errors_numeric()
    

@register_nbiot_action
class ActionNBIoTSetErrorsVerbose(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_errors_verbose",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            description="Set errors to be displayed in verbose (text) mode (CMEE=2)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_errors_verbose()
    
@register_nbiot_action
class ActionNBIoTSMSFormat(Action[ResultNBIoT[str]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="sms_format",
            result_type=ResultNBIoT[str],
            data_type=str,
            description="Get current SMS message format (CMGF?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[str]:
        return handler.get_sms_format()
    

@register_nbiot_action
class ActionNBIoTSetSMSFormatText(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_sms_format_text",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            description="Set SMS message format to text (CMGF=1)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_sms_format_text()
    

@register_nbiot_action
class ActionNBIoTSetSMSFormatPdu(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="set_sms_format_pdu",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            description="Set SMS message format to PDU (CMGF=0)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.set_sms_format_pdu()
    
@register_nbiot_action
class ActionNBIoTSimReady(Action[ResultNBIoT[str]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="sim_ready",
            result_type=ResultNBIoT[str],
            data_type=str,
            description="Check if SIM is ready (CPIN?)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[str]:
        return handler.sim_ready()
    

@register_nbiot_action
class ActionNBIoTSimUnlock(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="sim_unlock",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            allowed_args={
                "password": ActionAgrument(arg_type=str, description="SIM password. Usually 4 digits")
            },
            description="Unlock SIM with password (CPIN=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.sim_unlock(**kwargs)


@register_nbiot_action
class ActionNBIoTSendSMS(Action[ResultNBIoT[str]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="send_sms",
            result_type=ResultNBIoT[str],
            data_type=str,
            allowed_args={
                "number": ActionAgrument(arg_type=str, description="Destination number"),
                "msg": ActionAgrument(arg_type=str, description="Message"),
            },
            description="Send SMS to provided number (CMGS=)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[str]:
        return handler.send_sms(**kwargs)
    

@register_nbiot_action
class ActionNBIoTGetUnreadSMS(Action[ResultNBIoT[list[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="get_unread_sms",
            result_type=ResultNBIoT[list[dict]],
            data_type=list[dict],
            description="Get all unread SMS messages (CMGL='REC UNREAD')" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[dict]]:
        return handler.get_unread_sms()
    

@register_nbiot_action
class ActionNBIoTGetAllSMS(Action[ResultNBIoT[list[dict]]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="get_all_sms",
            result_type=ResultNBIoT[list[dict]],
            data_type=list[dict],
            description="Get all SMS messages (CMGL='ALL')" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[list[dict]]:
        return handler.get_all_sms()
    

@register_nbiot_action
class ActionNBIoTDeleteAllSMS(Action[ResultNBIoT[bool]]):
    
    def __init__(self) -> None:
        super().__init__(
            identifier="delete_all_sms",
            result_type=ResultNBIoT[bool],
            data_type=bool,
            description="Delete all SMS messages (CMGD=1,1)" 
        )

    def _action(self, handler: ProtocolHandlerNBIoT, **kwargs) -> ResultNBIoT[bool]:
        return handler.delete_all_sms()