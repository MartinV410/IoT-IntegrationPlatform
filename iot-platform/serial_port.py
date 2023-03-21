import serial
from utils import Result
import time


class SerialPort:
    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1) -> None:
        self.__serial = None
        self.__port = port
        self.__baudrate = baudrate
        self.__timeout = timeout

    def close(self) -> None:
        if self.__serial is not None:
            self.__serial.close()
            self.__serial = None

    def __force_connect(self) -> Result[bool]:
        self.close()
        return self.__connect()


    def __connect(self) -> Result[bool]:
        """
        Connects to serial port that can send/receive messages throught bluetooth
        """
        if self.__serial is None or not self.__serial.is_open:
            try:
                self.__serial = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout)
                return Result[bool](passed=True, data=True, message=f"Serial on port '{self.__port}' connected")
            except serial.serialutil.SerialException as e:
                self.__serial = None
                return Result[bool](passed=False, data=False, message=f"Cannot connect to serial on port '{self.__port}'!", error=e)
            except Exception as e:
                return Result[bool](passed=False, data=True, message=f"Could not write to serial on port '{self.__port}'! Unexpected error!", error=e)

        return Result[bool](passed=True, data=True, message="No need to connect. Already connected.")

    def __check_reconnect(self) -> Result[bool]:
        if self.__serial is None or not self.__serial.is_open:
            result = self.__connect()
            if not result.passed:
                return result
            
        return Result[bool](passed=True, data=True, message="Serial port OK")

    def __read(self, read_func, block: bool = True) -> Result[str]:
        check = self.__check_reconnect()

        if not check.passed:
            return Result[str](passed=check.passed, data=check.message, message=check.message)

        try:
            #buff = self.__serial.readline()
            self.__serial.reset_input_buffer()
            buff = b''
            if block:
                while not self.__serial.in_waiting: 
                    pass
                while self.__serial.in_waiting:
                    buff += read_func()
                    time.sleep(0.01)
                    
            else:
                buff = read_func()
                #print(f"New buff: {buff}")
            return Result[str](passed=True, data=buff.decode(), message=f"Result from serial buffer on port '{self.__port}'")
        except serial.serialutil.SerialException as e:
            self.__serial.close()
            return Result[str](passed=False, data="", message=f"Could not read from serial on port '{self.__port}'!", error=e)
        except Exception as e:
            return Result[str](passed=False, data="", message=f"Could not read from serial on port '{self.__port}'! Unexpected exception!", error=e)

    def read_line_noblock(self) -> Result[str]:
        #check = self.__force_connect()
        check = self.__check_reconnect()
        if not check.passed:
            return Result[str](passed=check.passed, data=check.message, message=check.message)
        return self.__read(read_func=self.__serial.readline, block=False)

    def read_all(self) -> Result[str]:
        check = self.__check_reconnect()
        if not check.passed:
            return Result[str](passed=check.passed, data=check.message, message=check.message)
        return self.__read(read_func=self.__serial.read_all)

    def write(self, msg: str) -> Result[bool]:
        if self.__serial is None or not self.__serial.is_open:
            result = self.__connect()
            if not result.passed:
                return result

        try:
            self.__serial.write(msg.encode())
            return Result[bool](passed=True, data=True, message=f"Write to serial buffer on port '{self.__port}' successful")
        except serial.serialutil.SerialException as e:
            return Result[bool](passed=False, data=True, message=f"Could not write to serial on port '{self.__port}'!", error=e)
        except Exception as e:
            return Result[bool](passed=False, data=True, message=f"Could not write to serial on port '{self.__port}'! Unexpected exception!", error=e)

        
