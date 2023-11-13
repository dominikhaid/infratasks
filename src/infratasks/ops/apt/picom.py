from pyinfra.operations import server, apt, git, files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class PicomOperation(Operation, AptUtil):
    name = "picom"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = ["pipx",
                "libxcb1-dev",
                "libxcb-damage0-dev",
                "libxcb-xfixes0-dev",
                "libxcb-dpms0-dev",
                "libxcb-util-dev",
                "libxcb-render-util0-dev",
                "libxcb-render0-dev",
                "libxcb-randr0-dev",
                "libxcb-composite0-dev",
                "libxcb-image0-dev",
                "libxcb-present-dev",
                "libxcb-xinerama0-dev",
                "libxcb-glx0-dev",
                "libpixman-1-dev",
                "libdbus-1-dev",
                "libconfig-dev",
                "libgl1-mesa-dev",
                "libpcre2-dev",
                "libpcre3-dev",
                "libevdev-dev",
                "uthash-dev",
                "libev-dev",
                "libx11-xcb-dev"]

    def configure_debian_amd64(self):
        apt.packages(
            name="Checking dependencies",
            present=True,
            packages=self.packages,
            _sudo=True
        )

        server.shell(
            name="Installing Meson trough pipx",
            commands=["pipx install meson --force"],
            _shell_executable="bash",
            _ignore_errors=False
        )

        files.link(
            name="Linking Meson bin",
            path='/usr/local/bin/meson',
            target="{}/.local/bin/meson".format("/home/dominik"),
            symbolic=True,
            present=True,
            _sudo=True,
            _ignore_errors=False
        )

        # TODO IF EXITING PULL ?
        git.repo(
            name="Clone Picom",
            src="https://github.com/yshui/picom.git",
            dest="/home/dominik/dev/picom",
        )

        server.shell(
            name="Building picom",
            commands=[
                "cd {} && git submodule update --init --recursive".format("/home/dominik/dev/picom"),
                "cd {} && meson --buildtype=release . build".format("/home/dominik/dev/picom"),
                "cd {} && ninja -C build".format("/home/dominik/dev/picom"),
                "cd {} && ninja -C build install".format("/home/dominik/dev/picom"),
            ],
            _sudo=True,
            _shell_executable="bash"
        )

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall {} Apt Packages".format(self.name.title()),
            packages=self.packages,
            present=False,
            _sudo=True
        )
