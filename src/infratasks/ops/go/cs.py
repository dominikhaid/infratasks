from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class CsOperation(Operation, OpsUtil):
    name = "cs"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("go")
        server.shell(
            name=self.print_name(None, True),
            commands=["export GO111MODULE='on' && go install github.com/boyter/cs@v1.3.0"],
        )

    def delete_debian_amd64(self):
        self.get_version("go")
        home = self.host_data["home"]
        if home:
            server.shell(
                commands=[f"rm  {home}/go/bin/{self.name}"],
                name=self.print_name(None, False),
                _ignore_errors=True
            )
