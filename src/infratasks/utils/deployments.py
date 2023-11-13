import importlib
import re

from pyinfra.api import deploy

from pyinfra import logger
from infratasks.utils.handler import Handler
from infratasks.utils.operations import OperationsPaser, OperationHandler
from infratasks.utils.parser import Parser, AbstractParseElement


class Deployment(AbstractParseElement):
    def __init__(self, name: str, operations: list[str] | None, configure=True, delete=False):
        super().__init__(name, configure, delete)
        self.name = name
        self.configure = configure
        self.delete = delete
        if operations is not None:
            self.operations = operations

    def execute(self, configure=True):
        ops_key = "ops"
        parser = OperationsPaser(ops_key)
        logger.info(f"Collecting operations for deployment {self.name}".upper())
        for operation in self.operations:
            if configure:
                parser.add_element_from_name(operation, True)
            else:
                parser.add_element_from_name(operation, False, True)


class DeploymentsPaser(Parser):
    parser_key: str
    parsed_elements: list[Deployment] = list()

    def load_module(self, name: str):
        return importlib.import_module(f"infratasks.deploys.{name}").__getattribute__(f"{name.title()}Deployment")

    def add_element_from_name(self, name: str, configure: bool, delete: bool = False):
        regex = re.compile(r'^[\w\d_]+\.[\w\d_]+$')
        if regex.match(name):
            return
        for op in self.parsed_elements:
            if op.name == name and op.configure == configure and op.delete == delete:
                return
        mod = self.load_module(name)
        element = mod(name, None, configure, delete)
        self.append_element(element)


class DeploymentHandler(Handler):

    @staticmethod
    def configure_element(element: Deployment):
        element.execute(configure=True)

    @staticmethod
    def delete_element(element: Deployment):
        element.execute(configure=False)

    @classmethod
    @deploy("deployment".upper())
    def execute(cls, element: Deployment | None, element_list: list[Deployment]):
        if element_list is not None:
            if element_list.__len__() == 0:
                ops_key = "ops"
                logger.info(f"Collecting operations from host.data {ops_key}".upper())
                OperationsPaser(ops_key)

            for element in element_list:
                cls.handle_element(element)

            parser = OperationsPaser(None)
            ops = parser.get_parsed_elements()
            logger.info(f"All deployments and operations are parsed".upper())
            OperationHandler.execute(None, ops)
        elif element is not None:
            ops_key = "ops"
            logger.info(f"Collecting operations from host.data {ops_key}".upper())
            parser = OperationsPaser(ops_key)
            cls.handle_element(element)
            ops = parser.get_parsed_elements()
            logger.info(f"All deployments and operations are parsed".upper())
            OperationHandler.execute(None, ops)
