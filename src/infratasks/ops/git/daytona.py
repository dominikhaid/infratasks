from pyinfra.operations import server, files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class DaytonaOperation(Operation, AptUtil):
    name = "daytona"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = [
        "daytona"
    ]

    def configure_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            files.download(
                name="Download Daytona",
                src="https://download.daytona.io/daytona/install.sh",
                dest=f"{home}/.local/bin/{self.name}",
                force=True
            )
            server.shell(
                commands=[f"chmod +x {home}/.local/bin/{self.name}"],
                name=self.print_name(None, True),
            )
            server.shell(
                commands=[f"export DAYTONA_PATH=\"{home}/.local/bin/\" && {home}/.local/bin/{self.name}"],
                name=self.print_name(None, True),
            )

    def delete_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            files.file(
                path=f"{home}/.local/bin/{self.name}",
                present=False
            )
