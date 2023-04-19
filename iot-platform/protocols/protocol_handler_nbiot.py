# from .protocol_handler import ProtocolHandler
from typing import List, Dict

from .handler import Handler
import time, logging
from serial_port import SerialPort
from utils import ResultNBIoT
from dataclasses import dataclass
from configs import ConfigNBIoT


# AT+CNMP=38
# AT+CMNB=?
# AT+CPSI?
# AT+CREG=1

CR = "\r\n"

@dataclass
class ATCommand:
    command: str
    value: str = ""
    keyname: str = ""
    description: str = ""
    delimiter: str = "+"
    cr: str = "\r"
    start: str = "AT"

    def construct(self) -> str:
        return f"{self.start}{self.delimiter}{self.command}{self.value}{self.cr}"


AT_COMMANDS = {
    # INFO
    "manufacturer": ATCommand("CGMI", keyname="manufacturer"),
    "model_number": ATCommand("CGMM", keyname="model_number"),
    "revision": ATCommand("CGMR", keyname="revision"),
    "supported_feautures": ATCommand("GCAP", keyname="supported_feautures"),
    "serial_baud": ATCommand("IPR?", keyname="serial_baud"),
    "full_functionality": ATCommand("CFUN?", keyname="full_functionality"),
    "ready": ATCommand("CPAS", keyname="ready"),
    "current_time": ATCommand("CCLK?", keyname="current_time"),
    "current_network": ATCommand("COPS?", keyname="current_network"),
    "sim_ready": ATCommand("CPIN?", keyname="sim_ready"),

    # ERRORS
    "set_errors_numeric": ATCommand("CMEE=1", keyname="set_errors_numeric"),
    "set_errors_verbode": ATCommand("CMEE=2", keyname="set_errors_verbode"),

    # SMS
    "set_sms_format_text": ATCommand("CMGF=1", keyname="set_sms_format_text"),
    "set_sms_format_pdu": ATCommand("CMGF=0", keyname="set_sms_format_pdu"),
    "get_sms_format": ATCommand("CMGF?", keyname="get_sms_format"),
    "get_sms_encoding": ATCommand("CSCS?", keyname="get_sms_encoding"),
    "set_sms_encoding_gsm": ATCommand('CSCS="GSM"', keyname="set_sms_encoding_gsm"),
    "set_sms_encoding_ucs2": ATCommand('CSCS="UCS2"', keyname="set_sms_encoding_ucs2"),
    # "send_sms": ATCommand("CMGS=", keyname="send_sms", ctrl_z=True),  # TODO dorobit moznoat zadania cisla, formatu cisla, msg

    # GPS
    "set_gps_power_on": ATCommand("CGNSPWR=1", keyname="set_gps_power_on"),
    "set_gps_power_off": ATCommand("CGNSPWR=0", keyname="set_gps_power_off"),
    "get_gps_power": ATCommand("CGNSPWR?", keyname="get_gps_power"),
    "start_gps_cold": ATCommand("CGNSCOLD", keyname="start_gps_cold"),
    "start_gps_warm": ATCommand("CGNSWARM", keyname="start_gps_warm"),
    "start_gps_hot": ATCommand("CGNSHOT", keyname="start_gps_hot"),
    "get_gps_inf": ATCommand("CGNSINF", keyname="get_gps_inf"),  # GNSS navigation information parsed from NMEA sentences
    "get_gps_gnss_info": ATCommand("SGNSCMD=?", keyname="get_gps_gnss_info"),  # 0 = modes (this unit supports none)

    # TODO network register and other stuff from https://m2msupport.net/m2msupport/network-registration/ and https://www.waveshare.com/wiki/File:SIM7070_SIM7080_SIM7090_Series_AT_Command_Manual_V1.03.pdf
}


class ProtocolHandlerNBIoT(Handler):
    def __init__(self, config: ConfigNBIoT) -> None:
        super().__init__("nb-iot", config)
        self.__serial = SerialPort(port=self._config.serial_port, baudrate=self._config.serial_baud, timeout=self._config.serial_timeout)
        self.__last_at = ATCommand

    def close(self) -> None:
        self.__serial.close()

    def __send_at(self, command: ATCommand) -> ResultNBIoT[bool]:
        """Sends AT command

        Args:
            command (ATCommand): AT command

        Returns:
            ResultNBIoT[bool]: Result
        """
        self.__last_at = command
        result = self.__serial.write(command.construct())
        if not result.passed:
            return ResultNBIoT[bool](passed=result.passed, data=result.data, message=f"Cannot read from device! Perhaps device is not connected?", error=result.error)
        return ResultNBIoT[bool](passed=result.passed, data=result.data, message=result.message, error=result.error)

    def __get_clear_list(self, lst: List[str]) -> List[str]:
        """Clears AT response list of "" and "OK"

        Args:
            lst (list[str]): AT response list

        Returns:
            list[str]: cleaned AT command list
        """
        cleaned = List[str]()
        for data in lst:
            if data != "" and data != "OK":
                cleaned.append(data)

        return cleaned

    def __response(self) -> ResultNBIoT[List[str]]:
        """Get response of last AT command

        Returns:
            ResultNBIoT[list[str]]: Result with AT command result list
        """
        result = self.__serial.read_all()
        if result.passed:
            data = result.data.split(CR)
            cleaned = self.__get_clear_list(data)
            if not "ERROR" in cleaned:
                return ResultNBIoT[List[str]](passed=True, data=cleaned, message=f"Response from AT command '{self.__last_at.command}' successful")
            return ResultNBIoT[List[str]](passed=False, data=list(), message=f"AT command '{self.__last_at.command}' returned error!", error=(cleaned[0] if len(cleaned) > 0 else ""))

        return ResultNBIoT[List[str]](passed=result.passed, data=list(), message=result.message, error=result.error)

    def __send_and_receive(self, command: ATCommand) -> ResultNBIoT[List[str]]:
        """Sends AT command and get it response

        Args:
            command (ATCommand): AT command

        Returns:
            ResultNBIoT[list[str]]: Result with AT command response
        """
        at_result = self.__send_at(command=command)
        if not at_result.passed:
            return ResultNBIoT[List[str]](passed=False, data=list(), message=at_result.message, error=at_result.error)

        # time.sleep(0.05) # TODO zlepsit implementaciu

        return self.__response()

    def __multiple_keynames(self, commands: List[ATCommand]) -> ResultNBIoT[Dict[str, List[str]]]:
        """Execute multiple commands and get theyr response in key: name format

        Args:
            commands (list[ATCommand]): list of AT commands to be executed

        Returns:
            ResultNBIoT[dict[str, list[str]]]: Result with key: name format result
        """
        info = Dict[str, str]()

        result = self.send_multiple_at(commands=commands)
        if not result.passed:
            return ResultNBIoT[Dict[str, str]](passed=False, data=Dict[str, str](), message=result.message, error=result.error)

        for command in commands:
            info[command.keyname] = result.data[command.construct()]

        return ResultNBIoT[Dict[str, List[str]]](passed=True, data=info, message="Multiple AT commands in keyname format")

    def send_and_receive_multiple(self, commands: List[ATCommand]) -> ResultNBIoT[Dict[str, List[str]]]:
        """Sends multiple AT commands. Return error Result as soon as one fail

        Args:
            commands (list[ATCommand]): AT commands

        Returns:
            ResultNBIoT[dict[str, list[str]]]: Result with list of commands results
        """
        results = Dict[str, List[str]]()

        for command in commands:
            result = self.__send_and_receive(command=command)
            if not result.passed:
                return ResultNBIoT[Dict[str, List[str]]](passed=False, data=results, message=result.message, error=result.error)
            results[command.construct()] = result.data

        return ResultNBIoT[Dict[str, List[str]]](passed=True, data=results, message=f"All AT commands were successful.")

    # https://m2msupport.net/m2msupport/at-commands-to-get-device-information/
    def device_info(self) -> ResultNBIoT[Dict[str, str]]:
        commands = [
            AT_COMMANDS["manufacturer"],
            AT_COMMANDS["model_number"],
            AT_COMMANDS["revision"],
            AT_COMMANDS["supported_feautures"],
            AT_COMMANDS["serial_baud"],
            AT_COMMANDS["full_functionality"],
            AT_COMMANDS["ready"],
            AT_COMMANDS["current_time"],
            AT_COMMANDS["sim_ready"]
        ]

        result = self.__multiple_keynames(commands=commands)
        if result.passed:
            return ResultNBIoT[Dict[str, str]](passed=True, data=result.data, message="NB-IoT device info")
        return ResultNBIoT[Dict[str, str]](passed=False, data=dict(), message=result.message, error=result.error)

    def test(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="", delimiter=""))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="AT commands working")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def preffered_celular_modes(self) -> ResultNBIoT[List[str]]:
        """Cellular modes like GSM, LTE....

        Returns:
            ResultNBIoT[list[str]]: List of supported modes
        """
        result = self.__send_and_receive(ATCommand(command="CNMP=?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="List of preffered celular modes")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def preffered_celular_mode_current(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CNMP?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Current preffered celular mode")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def set_preffered_celular_mode(self, mode: int) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CNMP=", value=str(mode)))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message=f"Preffered celular mode selected")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def preffered_celular_protocol_modes(self) -> ResultNBIoT[List[str]]:
        """Cellular protocols modes like CAT-M, NB-IOT...

        Returns:
            ResultNBIoT[list[str]]: List of supported modes
        """
        result = self.__send_and_receive(ATCommand(command="CMNB=?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="List of preffered celular protocol modes")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def preffered_celular_protocol_mode_current(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CMNB?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Current preffered celular protocol mode")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def set_preffered_celular_protocol_mode(self, mode: int) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CMNB=", value=str(mode)))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message=f"Preffered celular mode protocol selected")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def inquiring_ue_sysinfo(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CPSI?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Inquiring UE System Info")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def network_registration(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CREG?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Network registration status")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def set_network_registration(self, mode: int) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CREG=", value=str(mode)))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="Network registration set")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def phone_functionality_current(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CFUN?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Current phone functionality")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def phone_functionality(self, mode: str) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CFUN=", value=mode))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="Phone functionality set")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def signal_quality(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="CSQ"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Signal quality")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def operators_available(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="COPS=?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="List of available operators")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def operator_mode(self) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command="COPS?"))
        if result.passed:
            return ResultNBIoT[List[str]](passed=True, data=result.data, message="Current operator mode")
        return ResultNBIoT[List[str]](data=list(), message=result.message, error=result.error)

    def set_operator(self, mode: str) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="COPS=", value=mode))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="Operator mode set")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def set_errors_numeric(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CMEE=1"))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="Errors set to numeric")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def set_errors_verbose(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CMEE=2"))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="Errors set to verbose")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def get_sms_format(self) -> ResultNBIoT[str]:
        result = self.__send_and_receive(ATCommand(command="CMGF?"))
        if result.passed:
            return ResultNBIoT[str](passed=True, data=result.data[0], message="Current SMS format")
        return ResultNBIoT[str](data=False, message=result.message, error=result.error)

    def set_sms_format_text(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CMGF=1"))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="SMS format set to text")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def set_sms_format_pdu(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CMGF=0"))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="SMS format set to pdu")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def sim_ready(self) -> ResultNBIoT[str]:
        result = self.__send_and_receive(ATCommand(command="CPIN?"))
        if result.passed:
            return ResultNBIoT[str](passed=True, data=result.data, message="SIM ready state")
        return ResultNBIoT[str](data=False, message=result.message, error=result.error)

    def sim_unlock(self, password: str) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command="CPIN=", value=password))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="SIM unlocked")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)

    def send_sms(self, number: int, msg: str) -> ResultNBIoT[List[str]]:
        result = self.__send_and_receive(ATCommand(command=f'CMGS="{number}"'))
        if not result.passed:
            return ResultNBIoT[List[str]](data="", message=result.message, error=result.error)

        if len(result.data) > 0 and ">" in result.data[0]:
            self.__serial.write(f"{msg}{chr(26)}\r")
            response = self.__response()
            return response

        return ResultNBIoT[List[str]](data="", message="Unexpected error occured")

    def __format_sms(self, sms_data: list) -> List[dict]:
        data_list = list()
        data_cur = dict()
        req_data = False
        for data in sms_data:
            if "+CMGL:" in data:
                splitted = data.split(",")
                data_cur["from"] = splitted[2].replace('"', '')
                data_cur["date"] = splitted[3].replace('"', '') + " " + splitted[4].replace('"', '')
                req_data = True
                continue

            if not "AT+CMGS" in data and req_data:
                data_cur["message"] = data
                data_list.append(data_cur)
                data_cur = dict()
                req_data = False

        return data_list

    def get_unread_sms(self) -> ResultNBIoT[List[dict]]:
        result = self.__send_and_receive(ATCommand(command='CMGL="REC UNREAD"'))
        if not result.passed:
            return ResultNBIoT[List[dict]](data=[], message=result.message, error=result.error)
        data_list = self.__format_sms(result.data)
        return ResultNBIoT[List[dict]](passed=True, data=data_list, message="All unread SMS messages")

    def get_all_sms(self) -> ResultNBIoT[List[dict]]:
        result = self.__send_and_receive(ATCommand(command='CMGL="ALL"'))
        if not result.passed:
            return ResultNBIoT[List[dict]](data=[], message=result.message, error=result.error)
        data_list = self.__format_sms(result.data)
        return ResultNBIoT[List[dict]](passed=True, data=data_list, message="All SMS messages")

    def delete_all_sms(self) -> ResultNBIoT[bool]:
        result = self.__send_and_receive(ATCommand(command='CMGD=1,1'))
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="All SMS messages deleted")
        return ResultNBIoT[bool](data=False, message=result.message, error=result.error)