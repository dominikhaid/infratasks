from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class JqOperation(Operation, OpsUtil):
    name = "jq"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=["cargo install --locked --all-features --git https://github.com/ms-jpq/sad --branch senpai"],
            name=self.print_name(None, True),
        )

    def delete_debian_amd64(self):
        self.get_version("cargo")
        server.shell(
            commands=["cargo uninstall jq"],
            name=self.print_name(None, False),
            _ignore_errors=True
        )
