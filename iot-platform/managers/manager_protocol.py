from multiprocessing import Process, Event
from protocols.protocol_handler import ProtocolHandler, ProtocolReadable    
from actions.action import Action
from utils import Result
from typing import Any, TypeVar, Generic
import logging, time
from configs import Config
from threading import Thread, Lock


from .manager_actions import ManagerActions
from .manager_zmq_rep import ManagerZmqRep
from .manager_zmq_pub import ManagerZmqPub

PROTO_HANDLER = TypeVar('PROTO_HANDLER', bound=ProtocolHandler)
RESULT = TypeVar('RESULT', bound=Result)


class ManagerProtocol(Process, Generic[PROTO_HANDLER, RESULT]):
    def __init__(self, handler: PROTO_HANDLER, actions: dict[str, Action], config: Config, stop_event: Event, result_type: RESULT, identifier: str) -> None:
        super().__init__()
        self.daemon=True

        self.__handler = handler
        self.__actions = actions
        self.__event = stop_event
        self.__identifier = identifier
        self.__config = config

        self.__result = result_type

        self.__read_thread = Thread
        self.__lock = Lock()


    def run(self) -> None:
        logging.info(f"Starting manager for '{self.__identifier}'")
        handler = self.__handler(self.__config)
        manager_actions = ManagerActions[self.__result](self.__actions, self.__result)
        manager_zmq_rep = ManagerZmqRep[self.__result](self.__config.zmq_port, self.__result)


        if isinstance(handler, ProtocolReadable):
            logging.info(f"Starting message publishing for '{self.__identifier}'")
            self.__read_thread = Thread(target=self.__read, args=(self.__event, handler, self.__config, self.__lock))
            self.__read_thread.setDaemon(True)
            self.__read_thread.start()
            logging.info(f"Message publishing for '{self.__identifier}' started")

        logging.info(f"Manager for '{self.__identifier}' running")
        
        # MAIN EXECUTION LOOP (BREAK WITH EVENT)
        while not self.__event.is_set():
            message_r = manager_zmq_rep.receive()

            # CHECK IF MESSAGE WAS RECEIVED, IS SERIALIZABLE
            if not message_r.passed:  
                if not message_r.error: # if timeout occured
                    continue
                # when message is not json serializable or another unexpected error occured
                manager_zmq_rep.respond([message_r])
                continue
            
            actions_r = list()
            with self.__lock:
                actions_r = manager_actions.manage_actions(message_r.data, handler)
            manager_zmq_rep.respond(actions_r)

        # CLEANUP
        logging.info(f"Stopping manager for '{self.__identifier}'")

        if isinstance(handler, ProtocolReadable):
            logging.info(f"Stopping message publishing for '{self.__identifier}'")
            if self.__read_thread.is_alive():
                self.__read_thread.join()
            logging.info(f"Message publishing for '{self.__identifier}' stopped")

        handler.close()
        manager_zmq_rep.close()

        logging.info(f"Mmanager for '{self.__identifier}' stopped")

    
    def __read(self, stop_event: Event, handler: ProtocolReadable, config: Config, lock: Lock):
    
        manager_pub = ManagerZmqPub(config.zmq_port_pub)
        
        while not stop_event.is_set():
            result = None
            with lock:
                result = handler.read()

            if result and result.passed and result.data:
                manager_pub.publish(result.data)
            
            time.sleep(0.01)
            #time.sleep(1)

        manager_pub.close()


    def get_config(self) -> Config:
        return self.__config



        