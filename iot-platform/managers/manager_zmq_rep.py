import zmq, json
from typing import Any, TypeVar, Generic
from utils import Result


RESULT = TypeVar('RESULT', bound=Result)

class ManagerZmqRep(Generic[RESULT]):
    def __init__(self, port: int, result_type: RESULT) -> None:
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._poller = zmq.Poller()
        self._poller.register(self._socket, zmq.POLLIN)
        #poller.register(self.__event, zmq.POLLIN)
        self._socket.bind(f"tcp://127.0.0.1:{port}")

        self._result = result_type


    def close(self) -> None:
        self._socket.close()

    def receive(self) -> RESULT:

        pool_result = self._poller.poll(timeout=1000) # TODO skusit prerobit na flag, ktory by to ukoncoval
        if len(pool_result) > 0: # TODO skontrolovat pri viacerych konkurentnch requestov!!!!
            try:
                msg = self._socket.recv()
                return self._result[dict](passed=True, data=json.loads(msg), message="Received json message")
            except json.JSONDecodeError as e:
                return self._result[dict](data={}, message="Wrong message format provided! Expected valid JSON!", error=e)
            except Exception as e:
                return self._result[dict](data={}, message="Unexpected error while trying to receive message!", error=e)
        else :            
            return self._result[dict](data={}, message="No message to receive")
        
    def respond(self, result: list[RESULT]) -> None:
        if len(result) == 1:
            self._socket.send_string(result[0].json())
        else:
            self._socket.send_string(json.dumps([obj.to_dict() for obj in result], default=str))