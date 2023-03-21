from abc import abstractmethod, ABC
from utils import Result
from protocols.protocol_handler import ProtocolHandler
from protocols.handler import Handler

from typing import Any, TypeVar, Generic, List

RESULT = TypeVar('RESULT', bound=Result)
DATA = TypeVar('DATA')
HANDLER = TypeVar('HANDLER', bound=Handler)


class ActionAgrument:
    def __init__(self, arg_type: Any, description: str, optional: bool = False, options: List[Any] = list()) -> None:
        self.__arg_type = arg_type
        self.__optional = optional
        self.__description = description
        self.__options = options

    def arg_type(self) -> Any:
        return self.__arg_type

    def optional(self) -> bool:
        return self.__optional

    def description(self) -> str:
        return self.__description

    def options(self) -> List[Any]:
        return self.__options

    def in_options(self, value: Any) -> bool:
        if len(self.__options) == 0:
            return True
        
        if value in self.__options:
            return True
        
        return False
    
    def help(self) -> dict[str, str]:
        temp = dict()
        temp["type"] = self.__arg_type.__name__
        temp["optional"] = self.__optional
        temp["options"] = self.__options
        temp["description"] = self.__description
        return temp


class Action(Generic[RESULT]):

    def __init__(self, identifier: str, description: str, result_type: RESULT, data_type=DATA, standalone: bool = False, allowed_args: dict[str, ActionAgrument] = dict()) -> None:
        self._identifier = identifier
        self._standalone = standalone
        self._description = description
        self._allowed_args = allowed_args

        self._result = result_type
        self._data_type = data_type

        self._accepted_true = ["true", "on"]
        self._accepted_false = ["false", "off"]

    def identifier(self) -> str:
        return self._identifier
    
    def description(self) -> str:
        return self._description

    def standalone(self) -> bool:
        return self._standalone
    
    def __help_args(self) -> list[dict[str, str]]:
        temp = list()
        for key, value in self._allowed_args.items():
            temp_d = value.help()
            temp_d["name"] = key
            temp.append(temp_d)

        return temp


    def help(self) -> dict[str, Any]:
        temp = dict()
        temp["name"] = self._identifier
        temp["standalone"] = self._standalone
        temp["description"] = self._description
        temp["allowed_args"] = self.__help_args()

        return temp


    def __check_int(self, number: str) -> Result[bool]:
        try:
            int(number)
            return Result[bool](passed=True, data=True, message="String is integer")
        except ValueError:
            return Result[bool](data=False, message="String is not an integer!")
        

    def __check_float(self, number: str) -> Result[bool]:
        try:
            float(number)
            return Result[bool](passed=True, data=True, message="String is float")
        except ValueError:
            return Result[bool](data=False, message="String is not an float!")


    def __check_bool(self, string: str) -> Result[bool]:

        if string.lower() in self._accepted_true:
            return Result[bool](passed=True, data=True, message="String is true bool")
        if string.lower() in self._accepted_false:
            return Result[bool](passed=True, data=False, message="String is false bool")
        
        return Result[bool](data=False, message=f"Unsupported bool identifier '{string}'!", error=f"Unsupported bool identifier '{string}'! Supported only {self._accepted_true} and {self._accepted_false} or plain JSON bool object! This is not case sensitive")


    def __check_args(self, **kwargs) -> Result[bool]:

        for key, value in kwargs.items(): 
            arg = self._allowed_args.get(key)
            if not key in self._allowed_args: # checks for unexpected arguments
                return Result[bool](data=False, message=f"Unexpected argument '{key}' in action '{self._identifier}'!", error=f"Received unexpected argument '{key}' in action '{self._identifier}'!")
            if not isinstance(value, arg.arg_type()): # checks for wrong arg type (this can occur even when "10" == int or "true" == bool)

                if(arg.arg_type() is int):
                    int_r = self.__check_int(value)
                    if int_r.passed:
                        continue
                if(arg.arg_type() is float):
                    float_r = self.__check_float(value)
                    if float_r.passed:
                        continue

                if(arg.arg_type() is bool):
                    bool_r = self.__check_bool(value)
                    if not bool_r.passed:
                        return bool_r
                    else:
                        continue
                
                return Result[bool](data=False, message=f"Wrong argument type for argument '{key}' in action '{self._identifier}'!", error=f"Expected  type '{arg.arg_type()}' for argument '{key}' but got '{type(value)}' in action '{self._identifier}' instead!")

        missing = list()

        for key, value in self._allowed_args.items(): # check for missing args
            # if not value.optional() and not kwargs.get(key):
            if not value.optional() and not key in kwargs:
                missing.append(key)

        if len(missing) > 0:
            return Result[bool](data=False, message=f"Missing required argument in action '{self._identifier}'!", error=f"Missing required arguments: {missing} in action '{self._identifier}'!")

        return Result[bool](passed=True, data=True, message="All arguments are correct")


    def __retype_strs(self, **kwargs) -> Result[dict[str, Any]]:
        new_kwargs = {}
        for key, value in kwargs.items(): 
            arg = self._allowed_args[key]
            if arg.arg_type() == int:
                new_kwargs[key] = int(value)
                continue
            if arg.arg_type() == float:
                new_kwargs[key] = float(value)
                continue
            if arg.arg_type() == bool:
                if isinstance(value, bool):
                    new_kwargs[key] = value
                    continue
                if value.lower() in self._accepted_true:
                    new_kwargs[key] = True
                    continue
                if value.lower() in self._accepted_false:
                    new_kwargs[key] = False
                    continue
                
            new_kwargs[key] = value

        return Result[dict[str, Any]](passed=True, data=new_kwargs, message="All kwargs retyped")
        
    def __check_options(self, **kwargs) -> Result[bool]:
        for key, value in kwargs.items(): 
            arg = self._allowed_args[key]

            if not arg.in_options(value):
                return Result[bool](data=False, message=f"Option '{value}' not allowed for argument '{key}'! Allowed are {arg.options()}")
            
        return Result[bool](passed=True, data=True, message=f"All options in arguments are correct")


    @abstractmethod
    def _action(self, handler: Handler, **kwargs) -> RESULT:
        raise NotImplementedError


    def perform(self, handler: Handler, **kwargs) -> RESULT:
        result_arg = self.__check_args(**kwargs)
        if not result_arg.passed:
            return self._result(passed=False, data=self._data_type(), message=result_arg.message, error=result_arg.error)

        retyped = self.__retype_strs(**kwargs)

        options_check = self.__check_options(**retyped.data)
        if not options_check.passed:
            return self._result(data=self._data_type(), message=options_check.message, error=options_check.error)

        return self._action(handler, **retyped.data)
