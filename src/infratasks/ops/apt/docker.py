import re

from pyinfra import host
from pyinfra.operations import apt
from pyinfra.operations import files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class DockerOperation(Operation, AptUtil):
    name = "docker"
    configure = True
    delete = False
    packages = [
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "ca-certificates",
        "curl",
        "gnupg",
        "docker-buildx-plugin",
        "docker-compose-plugin"
    ]
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    @classmethod
    def check_docker_works(cls, status, stdout, stderr):
        command = "docker run hello-world"
        status, stdout, stderr = host.run_shell_command(
            command=command,
            sudo=cls.use_sudo(),
            use_sudo_password=cls.use_sudo_password(),
            sudo_user=cls.use_sudo_user(),
        )
        if status and "Hello from Docker!" not in stdout:
            raise Exception("`{}` did not work as expected".format(command))
        elif not status and "sh: 1: docker: not found" not in stderr:
            raise Exception("Docker is still running")

    def configure_debian_amd64(self):
        apt.key(
            name="Add the Docker apt gpg key if we need to",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src="https://download.docker.com/linux/debian/gpg",
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
                "deb [arch={}] https://download.docker.com/linux/"
                "{} {} stable".format(arch, linux_id, code_name)
            ),
            filename="{}".format(self.name),
        )

        apt.packages(
            name=self.print_name(None, True),
            update=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=True,
            _on_success=self.check_docker_works
        )

        self.systemd(True, True, True)

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=False,
            _on_success=self.check_docker_works
        )

        files.file(
            name="Remove {} from sources".format(self.name),
            path="/etc/apt/sources.list.d/{}.list".format(self.name),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
        )
