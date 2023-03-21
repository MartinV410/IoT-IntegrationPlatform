from .api_layer import ApiLayer
from multiprocessing import Event
from configs import ConfigWebsocket
import zmq.asyncio, zmq, asyncio, websockets, logging, json


class ApiLayerWs(ApiLayer):
    def __init__(self, stop_event: Event, config: ConfigWebsocket) -> None:
        super().__init__(stop_event=stop_event, config=config)

        self._description="Websocket API layer that forwards published messages throughth websocket"
        self._identifier = "websocket"
        self._config = config
        self._autostart = config.websocket_autostart

        logging.getLogger("websockets.server").setLevel(logging.ERROR)
        logging.getLogger("websockets.protocol").setLevel(logging.ERROR)

    def _run(self) -> None:
        asyncio.run(ManagerWebsocket(self._config.websocket_port, self._config.zmq_port_pub, self._event).start())


class ManagerWebsocket:
    def __init__(self, port: int, zmq_pub_port: int, stop_event: Event) -> None:
        self.__port = port
        self.__event = stop_event

        self.__clients = set()
        context = zmq.asyncio.Context()
        self.__socket = context.socket(zmq.SUB)
        self.__socket.connect(f"tcp://0.0.0.0:{zmq_pub_port}")
        self.__socket.setsockopt_string(zmq.SUBSCRIBE, "")

    async def __receive_msg(self) -> None:
        msg = await self.__socket.recv()

        try: # handle json data passthrough
            msg_json = json.loads(msg)
            websockets.broadcast(self.__clients, msg_json)
            return
        except json.JSONDecodeError:
            pass

        # websockets.broadcast(self.__clients, msg.decode().replace("\r\n", ""))
        websockets.broadcast(self.__clients, msg.decode().replace("\r\n", ""))



    async def __handler_new_client(self, ws_client) -> None:
        # Add ws_client to connected clients (this assumes that client will never send message)
        self.__clients.add(ws_client)
        try:
            await ws_client.wait_closed()
        finally:
            self.__clients.remove(ws_client)

    async def start(self) -> None:
        async with websockets.serve(self.__handler_new_client, host="0.0.0.0", port=self.__port):
            while not self.__event.is_set():
                await self.__receive_msg()