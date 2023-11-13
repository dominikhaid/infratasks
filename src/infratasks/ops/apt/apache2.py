from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class Apache2Operation(Operation, AptUtil):
    name = "apache2"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            update=self.should_apt_update(),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=["apache2"],
            present=True,
        )
        self.systemd(False, False, False, "nginx", "nginx")
        self.systemd(True, True, True)

    def delete_debian_amd64(self):
        self.systemd(False, False, False)
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=["apache2"],
            present=False,
        )
