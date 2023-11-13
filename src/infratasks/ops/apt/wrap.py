from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class WrapOperation(Operation, AptUtil):
    name = "wrap"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.deb(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            src="https://releases.warp.dev/stable/v0.2024.03.19.08.01.stable_01/warp-terminal_0.2024.03.19.08.01.stable.01_amd64.deb",
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages="warp-terminal",
            present=False
        )
