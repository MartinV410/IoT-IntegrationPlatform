from abc import ABC, abstractmethod
from multiprocessing import Process, Event
from configs import Config
from typing import Dict, Any

class ApiLayer(Process):
    def __init__(self, stop_event: Event, config: Config) -> None:
        super().__init__()
        self.daemon=True

        self._event = stop_event
        self._description = "Not defined"
        self._autostart = False
        self._identifier = "Not defined"
        self._config = config


    def description(self) -> str:
        return self._description
    
    def identifier(self) -> str:
        return self._identifier
    
    def autostart(self) -> bool:
        return self._autostart
    
    def info(self) -> Dict[str, Any]:
        info = dict()
        info["identifier"] = self._identifier
        info["description"] = self._description
        info["running"] = self.is_alive()
        #info["config"] = self._config.__dict__
        return info

    def run(self) -> None:
        while not self._event.is_set():
            self._run()

    @abstractmethod
    def _run(self) -> None:
        raise NotImplementedError