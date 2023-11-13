from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class WebiOperation(Operation, OpsUtil):
    name = "webi"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name=self.print_name(None, True),
            commands=["curl -sS https://webinstall.dev/webi | bash"],
        )

    def delete_debian_amd64(self):
        webi = self.get_version("webi")
        home = self.host_data["home"]
        if webi and home:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf {home}/.local/bin/webi"],
                _ignore_errors=True
            )
