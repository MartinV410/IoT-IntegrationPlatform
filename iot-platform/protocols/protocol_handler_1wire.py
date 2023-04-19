from pi1wire import Pi1Wire, Resolution
from pi1wire._sensor import OneWireInterface
import logging

from typing import List, Dict
from utils import Result1Wire
# from .protocol_handler import ProtocolHandler
from .handler import Handler
from configs import Config1Wire


class ProtocolHandler1Wire(Handler):
    def __init__(self, config: Config1Wire) -> None:
        super().__init__("1-wire", config)
        self.__1w = Pi1Wire()
        self.__available = list()
        self.__current_resolution = Resolution.X0_5

    def close(self) -> None:
        pass

    def find_available(self) -> Result1Wire[List[str]]:
        """
        Finds all available sensors and stores them. Check for errors in case some sensor is not valid
        """
        all_sensors = self.__1w.find_all_sensors()
        available = list()

        for sensor in all_sensors:
            try:
                sensor.change_resolution(self.__current_resolution)
                available.append(sensor)
            except Exception as e:  # TODO change Exception
                return Result1Wire[List[str]](data=[], message="Available 1-Wire devices discovery failed!", error=e)

        self.__available = available

        res = [interface.mac_address for interface in available]
        return Result1Wire[List[str]](passed=True, data=res,
                                      message="Available 1-Wire devices discovery was successful.")

    def get_temperature(self, sensor_mac: str) -> Result1Wire[float]:
        """Get temperature of given sensor

        Args:
            sensor_mac (str): mac address of sensor

        Returns:
            Result[float]: result with temperature
        """
        self.find_available()
        sensor = self.__get_sensor(sensor_mac)

        if sensor is not None:
            try:
                return Result1Wire[float](passed=True, data=sensor.get_temperature(),
                                          message=f"Temperature of sensor '{sensor_mac}'.")
            except Exception as e:  # TODO change Exception
                return Result1Wire[float](data=0.0,
                                          message=f"Unexpected error while trying to get temperature of '{sensor_mac}'!",
                                          error=e)

        return Result1Wire[float](data=0.0, message=f"Cannot found sensor '{sensor_mac}'!")

    def get_temperatures(self) -> Result1Wire[List[Dict[str, float]]]:
        """Get temperatures of all available sensors

        Returns:
            Result[list[dict[str, float]]]: result with list of all temperatures
        """
        self.find_available()
        temps = list()

        for sensor in self.__available:
            try:
                temps.append({sensor.mac_address: sensor.get_temperature()})
            except Exception as e:  # TODO change Exception
                logging.debug(f"Error while trying to retrieve temp from '{sensor.mac_address}'!")

        return Result1Wire[List[Dict[str, float]]](passed=True, data=temps,
                                                   message="Temperatures of all available sensors.")

    def change_resolution(self, sensor_mac: str, resolution: Resolution) -> Result1Wire[bool]:
        """Change sensing resolution of sensor

        Args:
            sensor_mac (str): mac address of sensor
            resolution (Resolution): resolution

        Returns:
            Result[bool]: if success or no
        """
        self.find_available()
        sensor = self.__get_sensor(sensor_mac)

        if sensor is not None:
            try:
                sensor.change_resolution(resolution=resolution)
                return Result1Wire[bool](passed=True, data=True,
                                         message=f"Resolution of {sensor_mac} changed to {resolution.value}")
            except Exception as e:  # TODO change Exception
                return Result1Wire[bool](data=False, message=f"Unexpected error while trying to set resolution!",
                                         error=e)

        return Result1Wire[bool](data=False, message=f"Cannot find sensor {sensor_mac}")

    def change_resolution_all(self, resolution: Resolution) -> Result1Wire[bool]:
        """Change sensing resolution of all available devices

        Args:
            resolution (Resolution): resolution

        Returns:
            Result[bool]: is success or no
        """
        self.find_available()
        for sensor in self.__available:
            try:
                sensor.change_resolution(resolution=resolution)
            except Exception as e:  # TODO change Exception
                return Result1Wire[bool](data=False,
                                         message=f"Unexpected error while trying to change resolution of sensors!",
                                         error=e)
        self.__current_resolution = resolution
        return Result1Wire[bool](passed=True, data=True, message=f"Changed resolution of all sensors.")

    def __get_sensor(self, sensor_mac: str) -> OneWireInterface:
        self.find_available()
        for sensor in self.__available:
            if sensor.mac_address == sensor_mac:
                return sensor

        return None
