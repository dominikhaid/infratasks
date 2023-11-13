from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class SdkmanOperation(Operation, OpsUtil):
    name = "sdkman"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name=self.print_name(None, True),
            commands=["curl -s https://get.sdkman.io | bash "],
        )

        home = self.host_data["home"]
        if home:
            server.shell(
                name=self.print_name(None, True),
                commands=[f"chmod +x {home}/.sdkman/bin/sdkman-init.sh",
                          f"{home}/.sdkman/bin/sdkman-init.sh",
                          f"sed -i -e 's/sdkman_auto_answer=false/sdkman_auto_answer=true/g' {home}/.sdkman/etc/config"],
            )

    def delete_debian_amd64(self):
        home = self.host_data["home"]

        if home:
            server.shell(
                name=self.print_name(None, False),
                commands=[f"rm -rf {home}/.sdkman"],
                _ignore_errors=True
            )
