from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class ChtshOperation(Operation, OpsUtil):
    name = "Chtsh"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name=self.print_name(None, True),
            commands=[
                "curl -s https://cht.sh/:cht.sh | sudo tee /usr/local/bin/cht.sh && sudo chmod +x /usr/local/bin/cht.sh"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
        )

    def delete_debian_amd64(self):
        server.shell(
            name=self.print_name(None, False),
            commands=["rm /usr/local/bin/cht.sh"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
            _ignore_errors=True
        )
