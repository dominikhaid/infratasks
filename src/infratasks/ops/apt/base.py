from pyinfra.operations import apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class BaseOperation(Operation, AptUtil):
    name = "base"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    pkg = [
        "apt-transport-https",
        "autoconf",
        "autojump",
        "automake",
        "expect",
        "bat",
        "build-essential",
        "ca-certificates",
        "clang",
        "cmake",
        "curl",
        "exa",
        "file-roller",
        "fonts-firacode",
        "fonts-noto-color-emoji",
        "g++",
        "gettext",
        "gnupg",
        "htop",
        "iputils-ping",
        "locales",
        "lsb-release",
        "neofetch",
        "net-tools",
        "ninja-build",
        "openssh-server",
        "pkg-config"
        "poppler-utils",
        "rfkill",
        "ripgrep",
        "rsync",
        "samba",
        "software-properties-common",
        "ssh",
        "sudo",
        "systemd",
        "tree",
        "ufw",
        "unzip",
        "vim",
        "vim-nox",
        "wget",
        "xpad",
        "zip",
    ],

    def configure_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            packages=self.pkg,
            update=self.should_apt_update(),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True
        )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            packages=self.pkg,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False
        )
