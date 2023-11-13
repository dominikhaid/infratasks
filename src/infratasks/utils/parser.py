import ast
from types import NoneType

from pyinfra import host
from pyinfra import logger


class AbstractParseElement:
    name: str
    configure: bool
    delete: bool

    def __init__(self, name: str, configure: bool, delete: bool):
        self.name = name
        self.configure = configure
        self.delete = delete


class Parser:
    parser_key: str
    parsed_elements: list[AbstractParseElement] = list()

    def __init__(self, parser_key: str | None):
        if not parser_key or parser_key.__len__() == 0:
            return
        self.parser_key = parser_key
        self.create_elements(parser_key)

    def add_element(self, element: AbstractParseElement):
        if not element:
            return
        self.parsed_elements.append(element)

    def add_element_from_name(self, name: str, configure: bool, delete: bool = False):
        mod = self.load_module(name)
        element = mod(name, configure, delete)
        self.append_element(element)

    def append_element(self, element: AbstractParseElement):
        if not element:
            return
        self.parsed_elements.append(element)

    def remove_element(self, ind: int):
        if ind < 0 or ind >= self.parsed_elements.__len__():
            return
        self.parsed_elements.pop(ind)

    def get_parsed_elements(self):
        excludes = host.data.get("exclude")
        includes = host.data.get("include")
        configures = host.data.get("configure")
        if excludes is not None:
            logger.info(f"Collecting data from host.data exclude".upper())
            for operation in self.parsed_elements:
                if isinstance(excludes, str) and operation.name == excludes:
                    self.parsed_elements.remove(operation)
                elif isinstance(excludes, list) and operation.name in excludes:
                    for exclude in excludes:
                        if operation.name == exclude:
                            self.parsed_elements.remove(operation)
        if isinstance(includes, str):
            logger.info(f"Collecting data from host.data include".upper())
            self.add_element_from_name(includes, True)
        if isinstance(includes, list):
            logger.info(f"Collecting data from host.data include".upper())
            for include in includes:
                self.add_element_from_name(include, True)
        if isinstance(includes, dict):
            logger.info(f"Collecting data from host.data include".upper())
            for key, conf in includes.items():
                self.add_element_from_name(key, conf.get("configure"), conf.get("delete"))
        if configures is not None:
            logger.info(f"Collecting data from host.data configure".upper())
            for operation in self.parsed_elements:
                if isinstance(configures, dict):
                    for key, conf in configures.items():
                        if operation.name == key:
                            operation.delete = conf.get("delete")
                            operation.configure = conf.get("configure")
        return self.parsed_elements  # TODO: REFACTOR

    def load_module(self, name: str):
        return AbstractParseElement

    def parse_dict(self, parsers_dict: dict[str, dict[str, bool] | bool]):
        for name, options in parsers_dict.items():
            if not name or name.__len__() == 0:
                continue
            configure, delete = self.parse_options(options)
            if isinstance(configure, NoneType) or isinstance(delete, NoneType):
                raise IOError(f"    can not parser for {name} from dict".upper())
            self.add_element_from_name(name, configure, delete)

    @staticmethod
    def parse_options(options: dict | bool):
        delete = False
        configure = False
        if isinstance(options, bool):
            if options is True:
                configure = True
            if options is False:
                delete = True
        if isinstance(options, dict):
            if options.__contains__("configure"):
                configure = options.get("configure")
            if options.__contains__("delete"):
                delete = options.get("delete")
            if not options.__contains__("delete") and configure is False:
                delete = True
        return configure, delete

    def parse_string(self, name: str):
        self.add_element_from_name(name, True)

    def parse_list(self, parsers_list: list):
        for name in parsers_list:
            if not name or name.__len__() == 0:
                continue
            self.load_module(name)
            self.add_element_from_name(name, True)

    def create_elements(self, parse_key: str):
        string_to_parse = host.data.get(parse_key)
        if not string_to_parse or self.parsed_elements.__len__() > 0:
            return
        logger.info(f"Collecting operations from host.data {parse_key}".upper())
        match type(string_to_parse).__name__:
            case "str":
                try:
                    string_to_parse = ast.literal_eval(string_to_parse)
                    host.data.__setattr__(parse_key, string_to_parse)
                except ValueError:
                    self.parse_string(string_to_parse)
                if isinstance(string_to_parse, dict):
                    self.parse_dict(string_to_parse)
                if isinstance(string_to_parse, list):
                    self.parse_list(string_to_parse)
            case "dict":
                self.parse_dict(string_to_parse)
            case "list":
                self.parse_list(string_to_parse)
            case _:
                raise IOError(f"    can not parse {string_to_parse}".upper())
