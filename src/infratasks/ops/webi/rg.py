from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class RgOperation(Operation, OpsUtil):
    name = "rg"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        webi = self.get_version("webi")
        if webi:
            server.shell(
                name=self.print_name(None, True),
                commands=[f"webi {self.name}@latest"],
            )

    def delete_debian_amd64(self):
        webi = self.get_version("webi")
        home = self.host_data["home"]
        if webi and home:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf /usr/bin/{self.name}",
                          f"rm -rf /usr/share/man/man1/{self.name}.1.gz", ],
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                _sudo_user=self.use_sudo_user(),
                _ignore_errors=True
            )
