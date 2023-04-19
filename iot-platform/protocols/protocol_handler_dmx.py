from typing import Any, Type, Dict, Union, List
from utils import ResultDMX
# from .protocol_handler import ProtocolHandler
from .handler import Handler
from configs import ConfigDMX
import serial, logging
from PyDMXControl.controllers import SerialController
from PyDMXControl.profiles.Generic import RGB_Vdim
from PyDMXControl.profiles.defaults import Fixture


class ProtocolHandlerDMX(Handler):
    def __init__(self, config: ConfigDMX) -> None:
        super().__init__("DMX", config)

        try:
            self.__dmx = SerialController(config.serial_port)
        except (serial.serialutil.SerialException, BrokenPipeError) as e:
            logging.critical(f"Manager for DMX cannot be started: {e}")


    def close(self) -> None:
        self.__dmx.close()

    def __check_range(self, value: int) -> ResultDMX[bool]:
        if 0 <= value <= 255:
            return ResultDMX[bool](passed=True, data=True, message=f"Value '{value}' is in range 0-255")
        return ResultDMX[bool](data=False, message=f"Value '{value}' is not in range 0-255!")

    def __check_range_list(self, values: List[int]) -> ResultDMX[bool]:
        for value in values:
            check = self.__check_range(value)
            if not check.passed:
                return check

        return ResultDMX[bool](passed=True, data=True, message="All values are in range 0-255")

    def __fixture_json(self, fixture: Union[Fixture, Type[Fixture]]) -> Dict:
        data = dict()
        data["id"] = fixture.id
        data.update(fixture.json_data)
        data.update(self.__fixture_channels(fixture))
        return data

    def __fixture_channels(self, fixture: Union[Fixture, Type[Fixture]]) -> Dict[str, int]:
        usage = dict()
        channel = fixture.channel_usage.split(" ")
        channel_usage = channel[0].split("->")

        usage["start_channel"] = int(channel_usage[0])
        usage["end_channel"] = int(channel_usage[1])
        usage["channels"] = int(channel[1].translate({ord('('): None, ord(')'): None}))

        return usage

    # FUNCTIONS ON ALL FIXTURES
    def add_fixture(self, fixture: Union[Fixture, Type[Fixture]], channel: int = -1, name: str = "") -> ResultDMX[bool]:
        try:
            if channel == -1:
                self.__dmx.add_fixture(fixture, name=name)
            else:
                self.__dmx.add_fixture(fixture, start_channel=channel, name=name)
        except Exception as e:
            return ResultDMX[bool](data=False, message="Error occured while creating a fixture!", error=e)

        return ResultDMX[bool](passed=True, data=True, message="New fixture was added")

    def all_locate(self) -> ResultDMX[bool]:
        if self.__dmx.get_all_fixtures() == 0:
            return ResultDMX[bool](data=False, message="No fixures to locate!")
        self.__dmx.all_locate()
        return ResultDMX[bool](passed=True, data=True, message="All fixures located")

    def all_fixtures(self) -> ResultDMX[List[dict]]:
        data = list()
        for fixture in self.__dmx.get_all_fixtures():
            data.append(self.__fixture_json(fixture))

        return ResultDMX[List[dict]](passed=True, data=data, message="Info about all fixtures")

    def all_on(self, delay: int = 0) -> ResultDMX[bool]:
        if self.__dmx.get_all_fixtures() == 0:
            return ResultDMX[bool](data=False, message="No fixures to turn on!")
        self.__dmx.all_on(milliseconds=delay)
        return ResultDMX[bool](passed=True, data=True, message="All fixtures turned on")

    def all_off(self, delay: int = 0) -> ResultDMX[bool]:
        if self.__dmx.get_all_fixtures() == 0:
            return ResultDMX[bool](data=False, message="No fixures to turn off!")
        self.__dmx.all_off(milliseconds=delay)
        return ResultDMX[bool](passed=True, data=True, message="All fixtures turned off")

    def all_color(self, red: int, green: int, blue: int, delay: int = 0) -> ResultDMX[bool]:
        if self.__dmx.get_all_fixtures() == 0:
            return ResultDMX[bool](data=False, message="No fixures to change color!")
        colors = [red, green, blue]

        check = self.__check_range_list(colors)
        if not check.passed:
            return check

        self.__dmx.all_color(colors, milliseconds=delay)
        return ResultDMX[bool](passed=True, data=True, message=f"All fixtures set to color {colors}")

    def all_dim(self, value: int, delay: int = 0) -> ResultDMX[bool]:
        if self.__dmx.get_all_fixtures() == 0:
            return ResultDMX[bool](data=False, message="No fixures to change color!")

        check = self.__check_range(value)
        if not check.passed:
            return check

        self.__dmx.all_dim(value=value, milliseconds=delay)
        return ResultDMX[bool](passed=True, data=True, message=f"All fixtures dimmed to {value}")

    def delete_fixture(self, fixture_id: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if fixture:
            fixture.off()
            self.__dmx.del_fixture(fixture_id)
            return ResultDMX[bool](passed=True, data=True, message=f"Fixture with id '{fixture_id}' deleted")
        return ResultDMX[bool](data=False, message=f"Fixture with id '{fixture_id}' not found!")

    def delete_all(self) -> ResultDMX[bool]:
        all_fixtures = self.__dmx.get_all_fixtures()
        if len(all_fixtures) == 0:
            return ResultDMX[bool](data=False, message="No fixtures to delete!")
        for fixture in self.__dmx.get_all_fixtures():
            fixture.off()
            self.__dmx.del_fixture(fixture.id)

        return ResultDMX[bool](passed=True, data=True, message="All fixtures deleted")

    # FUNCTIONS ON SINGLE FIXTURE
    def fixture_locate(self, fixture_id: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[bool](data=False, message=f"No fixture with id '{fixture_id}' found!")
        fixture.locate()
        return ResultDMX[bool](passed=True, data=True, message=f"Fixture '{fixture_id}' located")

    def fixture_on(self, fixture_id: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[bool](data=False, message=f"No fixture with id '{fixture_id}' found!")
        fixture.on()
        return ResultDMX[bool](passed=True, data=True, message=f"Fixture '{fixture_id}' turned on")

    def fixture_off(self, fixture_id: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[bool](data=False, message=f"No fixture with id '{fixture_id}' found!")
        fixture.off()
        return ResultDMX[bool](passed=True, data=True, message=f"Fixture '{fixture_id}' turned off")

    def fixture_dim(self, fixture_id: int, value: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[bool](data=False, message=f"No fixture with id '{fixture_id}' found!")

        range_r = self.__check_range(value)
        if not range_r.passed: return range_r
        fixture.dim(target_value=value)
        return ResultDMX[bool](passed=True, data=True, message=f"Fixture '{fixture_id}' dimmed to '{value}'")

    def fixture_color_set(self, fixture_id: int, red: int, green: int, blue: int) -> ResultDMX[bool]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[bool](data=False, message=f"No fixture with id '{fixture_id}' found!")

        colors = [red, green, blue]
        range_r = self.__check_range_list(colors)
        if not range_r.passed: return range_r
        fixture.color(color=colors)
        return ResultDMX[bool](passed=True, data=True, message=f"Fixture'{fixture_id}' changed color to {colors}")

    def fixture_color_get(self, fixture_id: int) -> ResultDMX[List[int]]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[List[int]](data=[], message=f"No fixture '{fixture_id}' found!")

        colors = fixture.get_color()
        return ResultDMX[List[int]](passed=True, data=colors, message=f"Fixture '{fixture_id}' color")

    def fixture_channels(self, fixture_id: int) -> ResultDMX[Dict[int, Dict]]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[Dict[int, Dict]](data={}, message=f"No fixture '{fixture_id}' found!")

        return ResultDMX[Dict[int, Dict]](passed=True, data=fixture.channels, message=f"Fixture '{fixture_id}' channels")

    def fixture_channel_usage(self, fixture_id: int) -> ResultDMX[Dict[str, int]]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[Dict[str, int]](data={}, message=f"No fixture '{fixture_id}' found!")

        return ResultDMX[Dict[str, int]](passed=True, data=self.__fixture_channels(fixture), message=f"Fixture '{fixture_id}' channel usage")

    def fixture_info(self, fixture_id: int) -> ResultDMX[Dict]:
        fixture = self.__dmx.get_fixture(fixture_id)
        if not fixture: return ResultDMX[Dict](data={}, message=f"No fixture '{fixture_id}' found!")

        return ResultDMX[Dict](passed=True, data=self.__fixture_json(fixture), message=f"Fixture '{fixture_id}' info")