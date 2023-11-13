from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class DotnetOperation(Operation, AptUtil):
    name = "dotnet"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = ["apt-transport-https",
                "dotnet-sdk-7.0",
                "dotnet-runtime-7.0",
                "aspnetcore-runtime-7.0"]

    def configure_debian_amd64(self):
        apt.deb(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            src="https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb",
        )

        apt.packages(
            name="Installing ASP NetCore",
            update=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            packages=self.packages,
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
            packages=self.packages,
        )
