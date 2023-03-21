import zmq, json
from typing import Any


class ManagerZmqPub:
    def __init__(self, port: int) -> None:
        context = zmq.Context()
        self._socket = context.socket(zmq.PUB)
        self._socket.bind(f"tcp://0.0.0.0:{port}")

    def close(self) -> None:
        self._socket.close()

    def publish(self, message: Any) -> None:
        if isinstance(message, str):
            self._socket.send_string(message)
        if isinstance(message, list):
            self._socket.send_json(json.dumps(message))
