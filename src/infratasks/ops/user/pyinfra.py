from pyinfra import host
from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class PyinfraOperation(Operation, OpsUtil):
    name = "pyinfra"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        pyinfra_user = host.data.infra_user_name
        sudo_user, stdout, stderr = host.run_shell_command(
            command=f"sudo -l -U {pyinfra_user}",
            sudo=True,
            use_sudo_password=True,
        )

        if not sudo_user:
            sudo_user_state = server.user(
                name=f"Ensure {pyinfra_user} user exists",
                user=f"{pyinfra_user}",
                shell="/bin/bash",
                group="sudo",
                add_deploy_dir=True,
                _sudo=self.use_sudo(),
                _use_sudo_password=True,
                ensure_home=True,
                unique=True,
                present=True,
                system=False
            )

            server.shell(
                name="Setting sudo password",
                commands=[f"echo '{pyinfra_user}:{pyinfra_user}' | sudo -S /usr/sbin/chpasswd;"],
                _sudo=self.use_sudo(),
                _use_sudo_password=True,
            )

    def delete_debian_amd64(self):
        pyinfra_user = host.data.infra_user_name
        sudo_user_state = server.user(
            name=f"Remove {pyinfra_user} user",
            user=f"{pyinfra_user}",
            present=False,
            _sudo=True,
            _use_sudo_password=True,
        )
