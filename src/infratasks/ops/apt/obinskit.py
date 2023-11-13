from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class ObinskitOperation(Operation, AptUtil):
    name = "obinskit"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        obinskit_version = self.version["obinskit"]
        if obinskit_version:
            apt.deb(
                name=self.print_name(None, True),
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                present=True,
                src=f"https://annepro.s3.amazonaws.com/ObinsKit_{obinskit_version}_x64.deb",
            )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.name,
            present=False,
        )
