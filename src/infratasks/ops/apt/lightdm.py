from pyinfra.operations import files
from pyinfra.operations import server, apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class LightdmOperation(Operation, AptUtil):
    name = "lightdm"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = ["lightdm", "expect", "light-locker", "slick-greeter", "lightdm-settings"]

    def configure_debian_amd64(self):
        installed = apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=True
        )

        if installed.changed:
            files.file(
                path="/etc/lightdm/lightdm.conf",
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                _sudo_user=self.use_sudo_user(),
                present=True
            )

            server.shell(
                name="Setting up {}".format(self.name.title()),
                commands=["sed -i 's/^greeter-session=.*//g' /etc/lightdm/lightdm.conf",
                          "sed -i 's/^\[Seat\:\*\]/[Seat:*]\\ngreeter-session=slick-greeter/g' /etc/lightdm/lightdm.conf"],
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                _sudo_user=self.use_sudo_user(),
            )

            server.shell(
                name="Reconfigure {}".format(self.name.title()),
                commands=["spawn  dpkg-reconfigure lightdm -freadline",
                          "expect \"2. lightdm\"",
                          "send \"2\r\""],
                _shell_executable="expect",
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                _sudo_user=self.use_sudo_user(),
            )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=False
        )

        server.shell(
            name="Cleaning up {}".format(self.name.title()),
            commands=["rm -rf /etc/lightdm"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
        )
