from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class NodeOperation(Operation, OpsUtil):
    name = "node"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        webi = self.get_version("webi")
        node_version = self.version["node"]
        if not node_version:
            node_version = "lts"
        if webi:
            server.shell(
                name=self.print_name(None, True),
                commands=[f"webi {self.name}@{node_version}"],
            )

    def delete_debian_amd64(self):
        webi = self.get_version("webi")
        home = self.host_data["home"]
        if webi and home:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf {home}/.local/opt/{self.name}",
                          f"rm -rf {home}/.local/bin/{self.name}"],
                _ignore_errors=True
            )
