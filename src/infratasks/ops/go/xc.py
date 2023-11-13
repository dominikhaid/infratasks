from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class XcOperation(Operation, OpsUtil):
    name = "xc"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        self.get_version("go")
        server.shell(
            name=self.print_name(None, True),
            commands=["export GO111MODULE='on' && go install github.com/joerdav/xc/cmd/xc@latest"],
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
