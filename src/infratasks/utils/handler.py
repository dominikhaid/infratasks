from pyinfra import logger
from pyinfra.api import deploy


class AbstractHandle:
    name: str
    configure: bool
    delete: bool

    def execute(self, configure: bool = True):
        pass


class Handler:
    @staticmethod
    @deploy("deployment skipped".upper())
    def skip_element(element: AbstractHandle):
        logger.info(f"skip {element.name}".upper())

    @staticmethod
    def configure_element(element: AbstractHandle):
        element.execute(configure=True)

    @staticmethod
    def delete_element(element: AbstractHandle):
        element.execute(configure=False)

    @classmethod
    def handle_element(cls, element: AbstractHandle):
        if not element.configure and not element.delete:
            cls.skip_element(element)
            return
        if element.delete:
            cls.delete_element(element)
        if element.configure:
            cls.configure_element(element)

    @classmethod
    def execute(cls, element: AbstractHandle | None, element_list: list[AbstractHandle]):
        if element_list is not None:
            for element in element_list:
                cls.handle_element(element)
        elif element is not None:
            cls.handle_element(element)
