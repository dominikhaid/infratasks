from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class AstreeOperation(Operation, OpsUtil):
    name = "astree"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("cargo")

        server.shell(
            name=self.print_name(None, True),
            commands=["cargo install -f --git https://github.com/jez/as-tree"],
        )

    def delete_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=["cargo uninstall as-tree"],
            name=self.print_name(None, False),
            _ignore_errors=True
        )
