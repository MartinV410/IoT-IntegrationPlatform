# https://m2msupport.net/m2msupport/software-and-at-commands-for-m2m-modules/

#   POSIELANIE SMS SPRAV
# 1.    AT+CREG? -- If device is not registered, SMS cannot be sent
# 2.    AT+CMGF? -- Get the current SMS Mode (0 – PDU Mode, 1- Text Mode) for SMS we want 1 - text mode
# 3.    AT+CMGF=1 -- First let us send SMS in text mode
# 4.    AT+CSCS? -- Check what type of sms-encoding is used. We want GSM
# 5.    AT+CSCS="GSM" -- Set sms-encoding

# BOLO POUZITE stty susp ^]

import time
from serial_port import SerialPort
from utils import ResultNBIoT
from dataclasses import dataclass

# port = serial.Serial(port="/dev/ttyUSB3", timeout=1, baudrate=9600)
# # port.write("AT\r".encode())
# # time.sleep(0.5)
# # port.write("AT\r\n".encode())
# # time.sleep(0.5)
# # port.write("AT\r\n".encode())
# # time.sleep(0.5)
# # port.write("AT\r\n".encode())
# # time.sleep(0.5)
# # port.write("AT\r\n".encode())
# # for i in range(5):
# #     port.write("AT\r\n".encode())
# #     time.sleep(0.5)
# #     print(port.read_all().decode().replace("\r\n", ""))

SERIAL_PORT = "/dev/ttyUSB3"
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 1
CR = "\r\n"
DELIMITER = "+"

@dataclass
class ATCommand:
    command: str
    params: str = list[str]
    keyname: str = ""
    description: str = ""
    delimiter: str = "+"
    cr: str = "\r"
    start: str = "AT"
    ctrl_z: bool = False

    def construct(self) -> str:
        ctrl_z = (f"{chr(26)}{self.cr}" if self.ctrl_z else "")
        return f"{self.start}{self.delimiter}{self.command}{self.params}{self.cr}{ctrl_z}"


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
    "send_sms": ATCommand("CMGS=", keyname="send_sms", ctrl_z=True), #TODO dorobit moznoat zadania cisla, formatu cisla, msg

    #GPS
    "set_gps_power_on": ATCommand("CGNSPWR=1", keyname="set_gps_power_on"),
    "set_gps_power_off": ATCommand("CGNSPWR=0", keyname="set_gps_power_off"),
    "get_gps_power": ATCommand("CGNSPWR?", keyname="get_gps_power"),
    "start_gps_cold": ATCommand("CGNSCOLD", keyname="start_gps_cold"),
    "start_gps_warm": ATCommand("CGNSWARM", keyname="start_gps_warm"),
    "start_gps_hot": ATCommand("CGNSHOT", keyname="start_gps_hot"),
    "get_gps_inf": ATCommand("CGNSINF", keyname="get_gps_inf"), #GNSS navigation information parsed from NMEA sentences
    "get_gps_gnss_info": ATCommand("SGNSCMD=?", keyname="get_gps_gnss_info"), # 0 = modes (this unit supports none)

    # TODO network register and other stuff from https://m2msupport.net/m2msupport/network-registration/ and https://www.waveshare.com/wiki/File:SIM7070_SIM7080_SIM7090_Series_AT_Command_Manual_V1.03.pdf
}


class HandlerNBIoT:
    def __init__(self) -> None:
        self.__serial = SerialPort(port=SERIAL_PORT, baudrate=SERIAL_BAUD, timeout=SERIAL_TIMEOUT)
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
        return ResultNBIoT[bool](passed=result.passed, data=result.data, message=result.message, error=result.error)

    def __get_clear_list(self, lst: list[str]) -> list[str]:
        """Clears AT response list of "" and "OK"

        Args:
            lst (list[str]): AT response list

        Returns:
            list[str]: cleaned AT command list
        """
        cleaned = list[str]()
        for data in lst:
            if data != "" and data != "OK":
                cleaned.append(data)

        return cleaned

    def __response(self) -> ResultNBIoT[list[str]]:
        """Get response of last AT command

        Returns:
            ResultNBIoT[list[str]]: Result with AT command result list
        """
        result = self.__serial.read_all()
        if result.passed:
            data = result.data.split(CR)
            cleaned = self.__get_clear_list(data)
            if not "ERROR" in cleaned:
                return ResultNBIoT[list[str]](passed=True, data=cleaned, message=f"Response from AT command '{self.__last_at.command}' successful")
            return ResultNBIoT[list[str]](passed=False, data=list(), message=f"AT command '{self.__last_at.command}' returned error!", error=(cleaned[0] if len(cleaned) > 0 else ""))


        return ResultNBIoT[list[str]](passed=result.passed, data=list(), message=result.message, error=result.error)

    def __send_and_receive(self, command: ATCommand) -> ResultNBIoT[list[str]]:
        """Sends AT command and get it response

        Args:
            command (ATCommand): AT command

        Returns:
            ResultNBIoT[list[str]]: Result with AT command response
        """
        at_result = self.__send_at(command=command)
        if not at_result.passed:
            return ResultNBIoT[list[str]](passed=False, data=list(), message=at_result.message, error=at_result.error)

        time.sleep(0.05) # TODO zlepsit implementaciu

        return self.__response()

    def __multiple_keynames(self, commands: list[ATCommand]) -> ResultNBIoT[dict[str, list[str]]]:
        """Execute multiple commands and get theyr response in key: name format

        Args:
            commands (list[ATCommand]): list of AT commands to be executed

        Returns:
            ResultNBIoT[dict[str, list[str]]]: Result with key: name format result
        """
        info = dict[str, str]()

        result = self.send_multiple_at(commands=commands)
        if not result.passed:
            return ResultNBIoT[dict[str, str]](passed=False, data=dict[str, str](), message=result.message, error=result.error)

        for command in commands:
            info[command.keyname] = result.data[command.construct()]

        return ResultNBIoT[dict[str, list[str]]](passed=True, data=info, message="Multiple AT commands in keyname format")

    
    def send_multiple_at(self, commands: list[ATCommand]) -> ResultNBIoT[dict[str, list[str]]]:
        """Sends multiple AT commands. Return error Result as soon as one fail

        Args:
            commands (list[ATCommand]): AT commands

        Returns:
            ResultNBIoT[dict[str, list[str]]]: Result with list of commands results
        """
        results = dict[str, list[str]]()

        for command in commands:
            result = self.__send_and_receive(command=command)
            if not result.passed:
                return ResultNBIoT[dict[str, list[str]]](passed=False, data=results, message=result.message, error=result.error)
            results[command.construct()] = result.data

        return ResultNBIoT[dict[str, list[str]]](passed=True, data=results, message=f"All AT commands were successful.")


    # https://m2msupport.net/m2msupport/at-commands-to-get-device-information/
    def device_info(self) -> ResultNBIoT[dict[str, str]]:
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
            return ResultNBIoT[dict[str, str]](passed=True, data=result.data, message="NB-IoT device info")
        return ResultNBIoT[dict[str, str]](passed=False, data=dict(), message=result.message, error=result.error)

    def send_sms(self, msg: str) -> ResultNBIoT[bool]:
        commands = [
            AT_COMMANDS["set_sms_format_text"],
            AT_COMMANDS["set_sms_encoding_gsm"],
            AT_COMMANDS["send_sms"],
        ]
        commands[2].params = msg

        result = self.__multiple_keynames(commands=commands)
        if result.passed:
            return ResultNBIoT[bool](passed=True, data=True, message="SMS was send successfuly")
        return ResultNBIoT[bool](passed=False, data=False, message=result.message, error=result.error)






nb = HandlerNBIoT()
print(nb.send_sms())




