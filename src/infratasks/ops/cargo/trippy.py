from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class TrippyOperation(Operation, OpsUtil):
    name = "trippy"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=[f"sudo cargo install {self.name}"],
            name=self.print_name(None, True),
        )

    def delete_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=[f"sudo cargo uninstall {self.name}"],
            name=self.print_name(None, False),
            _ignore_errors=True
        )
