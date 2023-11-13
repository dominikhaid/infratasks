from pyinfra.operations import server, apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class QemuOperation(Operation, AptUtil):
    name = "qemu"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = ["qemu-kvm",
                "libvirt-clients",
                "libvirt-daemon-system",
                "bridge-utils",
                "libguestfs-tools",
                "virtinst",
                "libosinfo-bin",
                "virt-manager",
                "genisoimage"]

    def configure_debian_amd64(self):
        installed = apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            latest=True,
            present=True
        )

        if (installed.changed):
            server.shell(
                name="Remove group libvirt-qemu",
                commands=["/sbin/delgroup libvirt-qemu"],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                _ignore_errors=True,
            )

            server.shell(
                name="Remove group libvirt",
                commands=["/sbin/delgroup libvirt"],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                _ignore_errors=True,
            )

            server.shell(
                name="Add group libvirt-qemu",
                commands=["/sbin/addgroup libvirt-qemu"],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
            )

            server.shell(
                name="Add group libvirt",
                commands=["/sbin/addgroup libvirt"],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
            )

            server.shell(
                name="Add user to libvirt",
                commands=["/sbin/adduser {} libvirt".format("dominik")],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
            )

            server.shell(
                name="Add user to libvirt-qemu",
                commands=["/sbin/adduser {} libvirt-qemu".format("dominik")],
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
            )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            update=self.should_apt_update(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.name,
            present=False,
        )

        server.shell(
            name="Remove group libvirt-qemu",
            commands=["/sbin/delgroup libvirt-qemu"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            _ignore_errors=True,
        )

        server.shell(
            name="Remove group libvirt",
            commands=["/sbin/delgroup libvirt"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            _ignore_errors=True,
        )

