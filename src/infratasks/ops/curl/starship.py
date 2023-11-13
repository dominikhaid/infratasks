from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class StarshipOperation(Operation, OpsUtil):
    name = "starship"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name=self.print_name(None, True),
            commands=["sh -c \"$(curl -fsSL https://starship.rs/install.sh)\" -- --yes"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
        )

    def delete_debian_amd64(self):
        server.shell(
            name=self.print_name(None, False),
            commands=["sh -c \"$(curl -fsSL https://starship.rs/uninstall.sh)\" -- --yes"],
            _ignore_errors=True
        )
