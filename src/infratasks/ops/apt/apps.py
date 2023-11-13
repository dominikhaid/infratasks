from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class AppsOperation(Operation, AptUtil):
    name = "apps"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = [
        "darktable",
        "evolution",
        "filezilla",
        "gparted",
        "gimp",
        # "gnome-disk-utility",
        # "gnome-keyring",
        # "gnome-software",
        # "gnome-system-tools",
        "i3lock",
        "inkscape",
        "krita",
        "libreoffice",
        "lxpolkit",
        "nitrogen",
        "notification-daemon",
        "pasystray",
        "pcmanfm",
        "pulseaudio-module-bluetooth",
        "remmina",
        "rofi",
        "systray-mdstat",
        "xfce4-power-manager",
        "xscreensaver",
    ]

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            update=self.should_apt_update(),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            packages=self.packages,
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
            packages=self.packages,
        )
