from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class InshellisenseOperation(Operation, OpsUtil):
    name = "inshellisense"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("npm")
        server.shell(
            name=self.print_name(None, True),
            commands=[f"npm install -g @microsoft/{self.name}"],
        )

    def delete_debian_amd64(self):
        self.get_version("go")
        home = self.host_data["home"]
        if home:
            server.shell(
                commands=[f"npm uninstall -g @microsoft/{self.name}"],
                name=self.print_name(None, False),
                _ignore_errors=True
            )
