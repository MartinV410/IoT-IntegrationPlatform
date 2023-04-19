from abc import abstractmethod, ABC
from typing import Any, TypeVar, Generic, Dict, List
from utils import Result
from actions.action import Action
from protocols.handler import Handler


RESULT = TypeVar('RESULT', bound=Result)


class ManagerActions(Generic[RESULT]):
    def __init__(self, actions: Dict[str, Action], result_type: RESULT) -> None:
        self._actions = actions
        self._result = result_type

    def _check_help(self, actions: Dict[str, dict]) -> RESULT:
        temp = list()
        if "help" in actions:
            if not isinstance(actions["help"], list):
                return self._result[List[dict]](data=[], message=f"Unexpected type for action 'help'!", error=f"Expected type 'list' but got '{type(actions['help']).__name__}' instead for action 'help'!")
            if len(actions["help"]) == 0: # if () (empty list) 
                for action in self._actions.values():
                    temp.append(action().help())
            else:
                for action in actions["help"]: # if actions are defined in help parameter
                    found_action = self._actions.get(action)
                    if not found_action:
                        return self._result[List[dict]](data=[], message="Unsupported action provided!", error=f"Received unsupported action '{action}'!")
                    temp.append(found_action().help())
            
            return self._result[List[dict]](passed=True, data=temp, message="Details of all available actions")
        return self._result[List[dict]](data=temp, message="Help action not found")

    def _check_actions(self, actions: Dict[str, dict]) -> RESULT:
        non_supp = list()

        for action in actions:
            if action not in self._actions:
                non_supp.append(action)
                continue
            if self._actions[action]().standalone():
                return self._result[bool](data=False, message=f"Action '{action}' is standalone! It can be issued only alone!")

        if len(non_supp) > 0:
            return self._result[bool](data=False, message=f"Unsupported action provided! Send 'help: []' for all available actions.", error=f"Received unsupported action {str(non_supp)}!")
        return self._result[bool](passed=True, data=True, message="All actions are valid")

    def _run_actions(self, actions: Dict[str, dict], handler: Handler) -> List[RESULT]:
        completed = list()

        for action, params in actions.items():
            if not isinstance(params, dict):
                return [self._result[bool](data=False, message=f"Unsupported argument type for action '{action}' provided!", error=f"Expected type 'dict' got '{type(params).__name__}'")]
            
            result = self._actions[action]().perform(handler=handler, **params)
            completed.append(result)
            if not result.passed:
                return completed
        
        return completed

    def manage_actions(self, actions: Dict[str, dict], handler: Handler) -> List[Result]:
        if len(actions) == 0:
            return [self._result[bool](data=False, message="No action to perform!")]

        # CHECK 'help' ACTION
        help_r = self._check_help(actions)
        if help_r.passed or help_r.error:  # if help was issued or error occured
            return [help_r]

        # CHECK PROVIDED ACTIONS IF THEYR VALID
        actions_r = self._check_actions(actions)
        if not actions_r.passed: # if unsupported action
            return [actions_r]

        # RUN ALL PROVIDED ACTIONS (THEY NEEDS TO BE CORRECT!!)
        run_r = self._run_actions(actions, handler)
        return run_r
