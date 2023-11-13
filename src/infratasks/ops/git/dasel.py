from pyinfra.operations import files
from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class DaselOperation(Operation, OpsUtil):
    name = "dasel"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            files.download(
                name="Download Dasel",
                src="https://github.com/TomWright/dasel/releases/download/v2.7.0/dasel_linux_amd64",
                dest=f"{home}/.local/bin/{self.name}",
                force=True
            )
            server.shell(
                commands=[f"chmod +x {home}/.local/bin/{self.name}"],
                name=self.print_name(None, True),
            )

    def delete_debian_amd64(self):
        self.get_version("go")
        home = self.host_data["home"]
        if home:
            server.shell(
                commands=[f"rm  {home}/.local/bin/{self.name}"],
                name=self.print_name(None, False),
                _ignore_errors=True
            )
