import pynmea2, time, logging
from utils import ResultNEO
from .handler import Handler
from configs import ConfigNEO
from serial_port import SerialPort

class ProtocolHandlerNEO(Handler):
    def __init__(self, config: ConfigNEO) -> None:
        super().__init__("NEO M8M", config)
        self.__serial_port = SerialPort(port=self._config.serial_port)

    def close(self):
        self.__serial_port.close()

    def position(self) -> ResultNEO[dict]:
        stop = False
        start = time.time()
        while not stop:
            if time.time() - start > 10:
                stop = True

            out_res = self.__serial_port.read_line_noblock()
            if out_res.passed:
                data = out_res.data

                if data[0:6]=='$GPRMC':
                    parsed=pynmea2.parse(data)
                    stop = True
                    return ResultNEO[dict](passed=True, data={"lat": parsed.latitude, "lng": parsed.longitude}, message="Latitude and longitude")
                
        return ResultNEO[dict](passed=False, data={}, message="Cannot retrieve latitude and longitude!", error="")
                
        