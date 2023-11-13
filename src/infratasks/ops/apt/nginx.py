from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class NginxOperation(Operation, AptUtil):
    name = "nginx"
    configure = True
    delete = False
    packages = ["nginx"]
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.name,
            present=True,
        )
        self.systemd(False, False, False, "apache2", "apache2")
        self.systemd(True, True, True)

    def delete_debian_amd64(self):
        self.systemd(False, False, False)
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.name,
            present=False,
        )
