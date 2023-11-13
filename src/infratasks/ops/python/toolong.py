from pyinfra.operations import server, apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class ToolongOperation(Operation, AptUtil):
    name = "toolong"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.packages(
            name="Checking {} dependencies".format(self.name.title()),
            packages=["pipx"],
            update=self.should_apt_update(),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True
        )

        server.shell(
            name="Installing {} with pipx".format(self.name.title()),
            commands=[f"pipx install {self.name}"],
        )

    def delete_debian_amd64(self):
        server.shell(
            name="Uninstalling {} with pipx".format(self.name.title()),
            commands=[f"pipx uninstall {self.name}"],
        )
