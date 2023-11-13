from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class VncOperation(Operation, AptUtil):
    name = "vnc"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = [
        "tightvncserver",
        "x11-xserver-utils",
        "x11vnc",
        "xserver-xorg",
        "xvfb"]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            update=self.should_apt_update(),
            packages=self.packages,
            present=True,
        )
        # TODO: copy files from template
        # self.systemd(True, True, True, "vncserver", "vncserver")

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.name,
            present=False,
        )
        self.systemd(False, False, False, "x11vnc", "x11vnc")
