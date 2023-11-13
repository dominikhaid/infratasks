import re

from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class GoOperation(Operation, OpsUtil):
    name = "go"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        webi = self.get_version("webi")
        if webi:
            server.shell(
                name=self.print_name(None, True),
                commands=[f"webi {self.name}-essentials@stable"],
            )

    def delete_debian_amd64(self):
        webi = self.get_version("webi")
        home = self.host_data["home"]
        go_version = self.get_version("go")
        if go_version:
            go_version = re.sub(r"go\sversion\sgo(\d?\d\.\d?\d?\w?\w?\d\.\d?\d).*", r"\1", go_version[0])

        if webi and home and go_version:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf {home}/.local/opt/{self.name}-v{go_version}",
                          f"rm -rf {home}/.local/bin/{self.name}-v{go_version}"],
                _ignore_errors=True
            )
