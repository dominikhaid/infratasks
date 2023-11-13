from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class DiveOperation(Operation, AptUtil):
    name = "dive"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        dive_version = self.version.get("dive")
        if not dive_version:
            raise Exception("dive version not found, please see help for more details")
        apt.deb(
            name="Installing Dive",
            src=f"https://github.com/wagoodman/dive/releases/download/v{dive_version}/dive_{dive_version}_linux_amd64.deb",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
        )

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall Dive",
            packages=["dive"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
        )
