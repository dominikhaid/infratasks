from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class RustOperation(Operation, OpsUtil):
    name = "rust"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name=self.print_name(None, True),
            commands=["cd ~/ && curl https://sh.rustup.rs -sSf | sh -s -- -y"],
        )

    def delete_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf /usr/lib/cargo ",
                          f"rm -rf {home}/.cargo",
                          f"rm -rf {home}/.rustup"],
                _ignore_errors=True
            )
