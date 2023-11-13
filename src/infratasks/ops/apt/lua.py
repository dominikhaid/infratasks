from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class LuaOperation(Operation, AptUtil):
    name = "lua"
    configure = True
    delete = False
    packages = ["lua5.4"]
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            latest=True,
            present=True
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=False,
        )
