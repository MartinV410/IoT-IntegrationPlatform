from bluetooth import BluetoothError
from enum import Enum
import subprocess, pexpect, bluetooth, time
from utils import ResultBluetooth
from .protocol_handler import ProtocolHandler, ProtocolReadable
from serial_port import SerialPort
from configs import ConfigBluetooth


#using doctring convention pep257
class Switchable(Enum):
    POWER = "power",
    PAIRABLE = "pairable",
    DISCOVERABLE = "discoverable",

SERIAL_PORT = "/dev/rfcomm0"


class ProtocolHandlerBluetooth(ProtocolHandler, ProtocolReadable):

    def __init__(self, config: ConfigBluetooth) -> None:
        super().__init__("bluetooth", config)
        #self.__socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.__bt_child = pexpect.spawn("bluetoothctl")
        self.__bt_child.sendline("agent off")
        self.__bt_child.sendline("agent NoInputNoOutput")
        self.__bt_child.sendline("scan on")

        self.__serial_port = SerialPort(port=self._config.serial_port)

    def close(self) -> None:
        self.__serial_port.close()
        self.__bt_child.close()
        

    def services(self, addr: str) -> ResultBluetooth[list[dict]]:
        """
        Displays services being advertised on a specified bluetooth device.
        Result.data (if device available and was found) has the following format:
        [
            {
                'service-classes': ['1801'], 
                'profiles': [], 
                'name': None, 
                'description': None, 
                'provider': None, 
                'service-id': None, 
                'protocol': 'L2CAP', 
                'port': 31, 
                'host': '80:9F:F5:36:A9:55'
            }, {...}
        ]

        Args:
            addr (str): mac address of bluetooth device

        Returns:
            ResultBluetooth[list[dict]]:Result with list of advertised services (empty list if device was not found)
        """
        if not self.is_on().data:
            return ResultBluetooth[list[dict]](passed=False, data=[{}], message=f"Cannot get services of '{addr}'! Bluetooth is off.")

        try:
            services = bluetooth.find_service(address=addr)
            return ResultBluetooth[list[dict]](passed=True,  data=services, message=f"Bluetooth services of '{addr}'")
        except BluetoothError as e:
            return ResultBluetooth[list[dict]](passed=False, data=[{}], message=f"Unexpected error while trying to get services of '{addr}'!", error=e)

        #return ResultBluetooth

    def discover_devices(self, duration: int, lookup_names: bool = True, lookup_class: bool = True) -> ResultBluetooth[list[dict]]: # TODO replace with pexpex implementation
        """
        Discover nearby available devices.
        ResultBluetooth.data has the following format (if lookup_names and classes are set to default):
        [
            {
                'addr': '80:9F:F5:34:A8:55', 
                'name': 'S21 používateľa Martin', 
                'class': 5898764
            }
        ]

        Args:
            duration (int): duration of discovery in seconds (longer discovery = more realiable ResultBluetooths)
            lookup_names (bool, optional): If name of device should be included in ResultBluetooth. Defaults to True.
            lookup_class (bool, optional): If class of device should be included in ResultBluetooth. Defaults to True.

        Returns:
            ResultBluetooth[list[dict]]:ResultBluetooth with list of discovered devices
        """
        if not self.is_on().data:
            return ResultBluetooth[list[dict]](passed=False, data=[{}], message=f"Cannot discover devices! Bluetooth is off.")

        nearby_devices = bluetooth.discover_devices(duration=duration, lookup_names=lookup_names, flush_cache=True, lookup_class=lookup_class)

        data = list()
        for device in nearby_devices:
            temp = dict()
            temp["addr"] = device[0]
            if lookup_names: temp["name"] = device[1]
            if lookup_class and lookup_names: temp["class"] = device[2]
            if lookup_class and not lookup_names: temp["class"] = device[1]

            data.append(temp)

        return ResultBluetooth[list[dict]](passed=True, data=data, message=f"Discovered bluetooth devices")

    def local_addr(self) -> ResultBluetooth[str]:
        """Returns local bluetooth mac address

        Returns:
            str: Local bluetooth mac address
        """
        if not self.is_on().data:
            return ResultBluetooth[str](passed=False, data="", message=f"Cannot get local address! Bluetooth is off.")

        return ResultBluetooth[str](passed=True, data=bluetooth.read_local_bdaddr()[0], message=f"Local bluetooth address")


    def __bluetoothctl_command(self, arg_list: list[str]) -> str:
        cmd = ["bluetoothctl"]
        cmd.extend(arg_list)
    
        command = subprocess.run(cmd, capture_output=True)
        return command.stdout.decode()

    def set_alias(self, new_alias: str) -> ResultBluetooth[bool]:
        """Change system bluetooth alias name 

        Args:
            new_alias (str): New alias

        Returns:
            ResultBluetooth[bool]: ResultBluetooth if succeeded or not
        """
        out = self.__bluetoothctl_command(["system-alias", f"'{new_alias}'"])
        out = out.replace("\n", "")
        if "succeeded" in out:
            return ResultBluetooth[bool](passed=True, data=True, message="New alias successfuly set.")
        return ResultBluetooth[bool](data=False, message=f"Alias could not be set!", error=out)

    def paired_devices(self) -> ResultBluetooth[list[dict]]:
        """Returns list of all paired devices. ResultBluetooth.data has the following format:
        [
            {
                'type': 'Device', 
                'addr': '80:9A:G5:34:A5:55', 
                'name': 'S21 používateľa Martin'
            }, {...}
        ]

        Returns:
            ResultBluetooth[list[dict]]: ResultBluetooth with list of paired devices
        """
        out = self.__bluetoothctl_command(["paired-devices"])
        lines = out.splitlines()
        result = list()
        for line in lines:
            spaces = line.split(" ")
            res = dict()
            res["type"] = spaces[0]
            res["addr"] = spaces[1]
            res["name"] = " ".join([n for n in spaces[2:]])

            result.append(res)

        return ResultBluetooth[list[dict]](passed=True, data=result, message="List of paired bluetooth devices.")

    def switch_function(self, function: Switchable, on: bool) -> ResultBluetooth[bool]:
        """Switch given functionality of bluetooth (for example discoverable, pairable...)

        Args:
            function (Switchable): function to be switched
            on (bool): switch function on/off

        Returns:
            ResultBluetooth[bool]: if switching was successfull
        """
        cmd = [function.value[0]]
        cmd.extend(["on"] if on else ["off"])
        out = self.__bluetoothctl_command(cmd)
        out = out.replace("\n", "")
        if "succeeded" in out:
            return ResultBluetooth[bool](passed=True, data=True, message=f"Switched {function.value[0]} to {('on' if on else 'off')}.")
        return ResultBluetooth[bool](data=False, message=f"Cannot switch {function.value[0]} {('on' if on else 'off')}!", error=out)

    def is_on(self) -> ResultBluetooth[bool]:
        """Checks if bluetooth is on

        Returns:
            ResultBluetooth[bool]: is/isnt powered 
        """
        out = self.__bluetoothctl_command(["show"])
        powered = out.splitlines()[4]

        if "yes" in powered:
            return ResultBluetooth[bool](passed=True, data=True, message="Bluetooth is on.")
        return ResultBluetooth[bool](passed=True, data=False, message="Bluetooth is off.")

    def is_discoverable(self) -> ResultBluetooth[bool]:
        """Checks if this device bluetooth is discoverable

        Returns:
            ResultBluetooth[bool]: is/isnt discoverable
        """
        out = self.__bluetoothctl_command(["show"])
        discoverable = out.splitlines()[5]

        if "yes" in discoverable:
            return ResultBluetooth[bool](passed=True, data=True, message="Device is discoverable.")
        return ResultBluetooth[bool](passed=True, data=False, message="Device is not discoverable.")

    def is_pairable(self) -> ResultBluetooth[bool]:
        """Checks if this device bluetooth is pairable

        Returns:
            ResultBluetooth[bool]: is/isnt pairable
        """
        out = self.__bluetoothctl_command(["show"])
        pairable = out.splitlines()[7]

        if "yes" in pairable:
            return ResultBluetooth[bool](passed=True, data=True, message="Device is pairable.")
        return ResultBluetooth[bool](passed=True, data=False, message="Device is not pairable.")

    def unpair(self, addr: str) -> ResultBluetooth[bool]:
        """Remove device from paired devices

        Args:
            addr (str): addres of device

        Returns:
            ResultBluetooth[bool]: if successful
        """
        out = self.__bluetoothctl_command(["remove", addr])
        out = out.replace("\n", "")
        if "has been removed" in out:
            return ResultBluetooth[bool](passed=True, data=True, message=f"Device '{addr}' was successfuly unpaired.")
        return ResultBluetooth[bool](data=False, message=f"Device '{addr}' cannot be unpaired!", error=out)

    def pair(self, addr: str) -> ResultBluetooth[bool]:
        """Pair to device with given address

        Args:
            addr (str): device address

        Returns:
            ResultBluetooth[bool]: If successful or not
        """
        self.__bt_child.sendline(f"pair {addr}")

        try:
            action = self.__bt_child.expect([".* not available", ".*AlreadyExists", "Failed to pair .*",  "Pairing successful"])
        except pexpect.exceptions.TIMEOUT:
            return ResultBluetooth[bool](data=False, message=f"Cannot pair device '{addr}'! Timeout!")

        if action == 0:
            return ResultBluetooth[bool](data=False, message=f"Cannot pair device '{addr}'! Device not available!")
        if action == 1:
            return ResultBluetooth[bool](data=False, message=f"Cannot pair device '{addr}'! Device already exists!")
        if action == 2:
            return ResultBluetooth[bool](data=False, message=f"Cannot pair device '{addr}'! Failed to pair!")
        if action == 3:
            return ResultBluetooth[bool](passed=True, data=True, message=f"Pairing of device '{addr}' successful!")

        return ResultBluetooth[bool](data=False, message=f"Cannot pair device '{addr}'! Unexpected error!")

    def read(self) -> ResultBluetooth[str]:
        """Read data from serial buffer of bluetooth

        Returns:
            str: Data from serial buffer ("" if empty)
        """
        result = self.__serial_port.read_line_noblock()

        if result.passed:
            return ResultBluetooth[str](passed=True, data=result.data, message="Read from bluetooth buffer successful")
        return ResultBluetooth[str](passed=False, data="", message=result.message, error=result.error)

    def write(self, message: str) -> ResultBluetooth[bool]:
        """Write data to serial buffer of bluetooth

        Args:
            message (str): Message to be send

        Returns:
            bool: If successful or no
        """
        result = self.__serial_port.write(message)

        if result.passed:
            return ResultBluetooth[bool](passed=True, data=True, message="Write to bluetooth buffer successful")
        return ResultBluetooth[bool](passed=False, data=False, message=f"Cannot write to bluetooth buffer! Perhaps no device is connected?", error=result.error)