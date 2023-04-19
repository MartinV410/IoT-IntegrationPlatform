from configs import Config
from configparser import ConfigParser
from utils import Result
import os, logging
from typing import Any, Dict


class ManagerConfig:
    def __init__(self, path: str) -> None:
        self.__parser = ConfigParser()
        self.__path = path
    
    def read(self) -> Result[bool]:
        if not os.path.exists(self.__path):
            logging.critical(f"Path to config file does not exists!")
            return Result[bool](data=False, message="Path to config file does not exists!")
        
        self.__parser.read(self.__path)
        return Result[bool](passed=True, data=True, message="Config read successful")

    def update(self, config_class: Config, identifier: str, values: Dict[str, Any]) -> Result[bool]:
        fields = self.__dataclass_to_dict(config_class)
        for key, value in values.items():
            if key not in self.__parser._sections[identifier]:
                return Result[bool](data=False, message=f"Received unexpected key '{key}' in '{identifier}'!")
            if not isinstance(value, fields[key]):
                return Result[bool](data=False, message=f"Expected type '{fields[key].__name__}' but got '{type(value).__name__}' instead for key '{key}'!")

        for key, value in values.items():
            self.__parser.set(identifier, key, str(value))
        
        with open(self.__path, "w") as file:
            self.__parser.write(file)

        return Result[bool](passed=True, data=True, message=f"New config for '{identifier}' is saved!")

    def __check_section(self, section: str) -> Result[bool]:
        if section not in self.__parser._sections: # if identifier has section in config
            return Result[bool](data=False, message=f"Section for '{section}' not found in config!")
        return Result[bool](passed=True, data=True, message=f"Section '{section}' found in config")

    def __check_fields(self, required: dict, provided: dict) -> Result[bool]:
        not_found = list()
        for key in required:
            if key not in provided:
                not_found.append(key)

        if len(not_found) > 0:
            return Result[bool](data=False, message=f"Required fields {not_found} not provided!")

        for key in provided:
            if key not in required:
                return Result[bool](data=False, message=f"Unexpected field '{key}' provided!")
        
        return Result[bool](passed=True, data=True, message=f"All required fields providet")

    def __construct_config(self, config_class: Config, section: str) -> Result[Config]:
        kwargs = {}
        section_dict = self.__parser._sections[section]
        for key, value in self.__dataclass_to_dict(config_class).items():
            try:
                if value is bool:
                    kwargs[key] = self.__parser[section].getboolean(key)
                    continue
                if value is float:
                    kwargs[key] = float(section_dict[key])
                    continue
                if value is int:
                    kwargs[key] = int(section_dict[key])
                    continue
                if value is str:
                    kwargs[key] = str(section_dict[key])
                    continue
            except ValueError as e:
                return Result[Config](data=None, message=f"Expected type '{value.__name__}' but got '{type(section_dict[key]).__name__}' instead for '{key}'!", error=e)

        return Result[Config](passed=True, data=config_class(**kwargs), message="Successfuly constructed config")

    def __dataclass_to_dict(self, config_class: Config) -> Dict[str, type]:
        temp = dict()

        for key, field in config_class.__dict__["__dataclass_fields__"].items():
            temp[key] = field.type
        return temp

    def get_config(self, config_class: Config, identifier: str) -> Result[Config]:

        section_r = self.__check_section(identifier)
        if not section_r.passed:
            logging.critical(section_r.message)
            return Result[Config](data=None, message=section_r.message, error=section_r.error)

        fields_r = self.__check_fields(self.__dataclass_to_dict(config_class), self.__parser._sections[identifier])
        if not fields_r.passed:
            logging.critical(fields_r.message)
            return Result[Config](data=None, message=fields_r.message, error=fields_r.error)
        
        return self.__construct_config(config_class, identifier)
        




