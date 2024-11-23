import importlib
import re

from pyinfra import host
from pyinfra import logger

from infratasks.utils.handler import Handler
from infratasks.utils.os import OsUtil
from infratasks.utils.parser import Parser, AbstractParseElement


class Operation(AbstractParseElement):
    def __init__(self, name: str, candidates: list[dict[str, str]] | None, host_data: dict[str, str] | None,
                 configure: bool = True, delete: bool = False):
        super().__init__(name, configure, delete)
        try:
            self.name = name.split(".")[1]
            self.pkg = name.split(".")[0]
        except IndexError:
            raise IndexError(f"    can not parse {name} to operation, format must be pkg.name".upper())
        self.configure = configure
        self.delete = delete
        self.host_data = OsUtil(host).get_host_data()
        self.version = OsUtil(host).get_versions()
        self.git_opts = OsUtil(host).get_git_opts()
        if candidates:
            self.candidates = candidates
        if host_data:
            self.host_data = host_data

    def execute(self, configure: bool = True):
        new_candidate = self.get_candidate(self.candidates, self.host_data)
        if new_candidate and isinstance(new_candidate, dict):
            self.execute_candidate(new_candidate, configure)
        else:
            logger.info(f"No install candiate for {self.name} {self.host_data.get('os_version')}".upper())
            pass

    def execute_candidate(self, new_candidate: dict[str, str], configure: bool = True):
        if new_candidate.get("os") == "Linux" and new_candidate.get("linux_name") == "Debian" and new_candidate.get(
                "os_version").__contains__("amd64"):
            if configure:
                self.configure_debian_amd64()
            else:
                self.delete_debian_amd64()
        if new_candidate.get("os") == "Windows" and new_candidate.get("os_version").__contains__("amd64"):
            if configure:
                self.configure_win_amd64()
            else:
                self.delete_win_amd64()

    @staticmethod
    def get_candidate(candidates: list[dict[str, str]], host_data: dict[str, str]) -> dict[str, str] | None:
        for candidate in candidates:
            if (candidate.get("os") == host_data.get("os") and candidate.get("linux_name") == host_data.get(
                    "linux_name") and host_data.get("os_version").__contains__(candidate.get("os_version"))):
                return candidate
            elif (not candidate.__contains__("linux_name") and candidate.get("os") == host_data.get("os")
                  and host_data.get("os_version").__contains__(candidate.get("os_version"))):
                return candidate
        return None

    def configure_defaults(self):
        pass

    def configure_debian_amd64(self):
        pass

    def delete_debian_amd64(self):
        pass

    def configure_win_amd64(self):
        pass

    def delete_win_amd64(self):
        pass


class OperationsPaser(Parser):
    parser_key: str
    parsed_elements: list[Operation] = list()

    def __init__(self, parser_key: str | None):
        if not parser_key or parser_key.__len__() == 0:
            return
        super().__init__(parser_key)
        self.parser_key = parser_key
        self.create_elements(parser_key)

    def load_module(self, name: str):
        try:
            pkg = name.split(".")[0]
            name = name.split(".")[1]
            return importlib.import_module(f"infratasks.ops.{pkg}.{name}").__getattribute__(
                f"{name.title()}Operation")
        except IndexError:
            raise IndexError(f"    can not parse {name} to operation, format must be pkg.name".upper())

    def add_element_from_name(self, name: str, configure: bool, delete: bool = False):
        regex = re.compile(r'^[\w\d_]+\.[\w\d_]+$')
        if not regex.match(name):
            return
        pkg = name.split(".")[0]
        title = name.split(".")[1]
        for op in self.parsed_elements:
            if op.name == title and pkg == op.pkg and op.configure == configure and op.delete == delete:
                return

        mod = self.load_module(name)
        element = mod(name, None, None, configure, delete)
        logger.info(f"Add operation {title}".upper())
        self.append_element(element)


class OperationHandler(Handler):

    @staticmethod
    def configure_element(element: Operation):
        element.execute(configure=True)

    @staticmethod
    def delete_element(element: Operation):
        element.execute(configure=False)
