from pyinfra.operations import apt
from pyinfra.operations import server

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class UfwOperation(Operation, AptUtil):
    name = "ufw"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            packages=["ufw"],
        )

        server.shell(
            name="Allow SSH",
            commands=["ufw allow 22"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        server.shell(
            name="Allow HTTP",
            commands=["ufw allow 80"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        server.shell(
            name="Allow HTTPS",
            commands=["ufw allow 443"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        server.shell(
            name="Allow VNC",
            commands=["ufw allow 5901", "ufw allow 5900"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
            packages=["ufw"],
        )
