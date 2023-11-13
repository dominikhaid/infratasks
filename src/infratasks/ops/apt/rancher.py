import re

from pyinfra import host
from pyinfra.operations import apt, server

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class RancherOperation(Operation, AptUtil):
    name = "rancher"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.sysctl(
            name="Set unprivileged port 80 for Traffic",
            key="net.ipv4.ip_unprivileged_port_start",
            value=80,
            persist=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        apt.key(
            name="Add the {} gpg Key".format(self.name.title()),
            src="https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/Release.key",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        lsb_info = self.host_data["lsb_release"]
        arch = re.sub(r'^\d\.\d\.\d-\d\d-', "", self.host_data["os_version"])
        linux_id = lsb_info["id"].lower()
        code_name = lsb_info["codename"]

        apt.repo(
            name="Add the Docker CE apt repo",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src=(
                "deb [arch={}] https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/ ./".format(arch)
            ),
            filename="{}".format(self.name),
        )

        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
            packages=["rancher-desktop", "pass"],
            update=True
        )

        command = "usermod -a -G docker $USER"
        host.run_shell_command(
            command=command,
            sudo=self.apt_use_sudo(),
            use_sudo_password=self.apt_use_sudo_password(),
            sudo_user=self.apt_use_sudo_user(),
        )

        # command="gpg --generate-key"
        # status, stdout, stderr = host.run_shell_command(
        #     command=command,
        #     sudo=self.apt_use_sudo(),
        #     use_sudo_password=self.apt_use_sudo_password(),
        #     sudo_user=self.apt_use_sudo_user(),
        # )

        # https://www.passwordstore.org/
        # TODO excpected dominik haid/info@dominikhaid.de/f -> pub
        # TODO kubectl kubens kubectx
        # print(status, stdout,stderr)
        # if not status or not stdout or stdout == "":
        #     raise Exception("`{}` did not work as expected".format(command))
        # server.shell(
        #     name="Add user to {} group".format(self.name.title()),
        #     commands=[f"pass init {stdout}"],
        #     _sudo=self.apt_use_sudo(),
        #     _use_sudo_password=self.apt_use_sudo_password(),
        #     _sudo_user=self.apt_use_sudo_user(),
        # )

        # TODO KUBECTL KUBENS KUBECTX HELM HELMFILE ARGO-CD-CLI VAULT-CLI

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall {} Apt Packages".format(self.name.title()),
            packages=["rancher-desktop", "pass"],
            present=False,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )
