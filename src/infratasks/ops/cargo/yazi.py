from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class YaziOperation(Operation, OpsUtil):
    name = "yazi-fm"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=[f"cargo install --locked --git https://github.com/sxyazi/yazi.git"],
            name=self.print_name(None, True),
        )

    def delete_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=[f"cargo uninstall {self.name}"],
            name=self.print_name(None, False),
            _ignore_errors=True
        )
