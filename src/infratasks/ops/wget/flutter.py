from pyinfra.operations import server, git, files

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class FlutterOperation(Operation, OpsUtil):
    name = "flutter"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            files.directory(
                path=f"{home}/dev/flutter",
                present=False,
                _on_success=self.install_debian_amd64,
            )

    def install_debian_amd64(self, state, stdout, stderr):
        home = self.host_data["home"]
        if home:
            git.repo(
                name="Clone {} Repo".format(self.name.title()),
                branch="stable",
                src="https://github.com/flutter/flutter.git",
                dest=f"{home}/dev/flutter",
            )

            server.shell(
                name=self.print_name(None, True),
                commands=[f"{home}/dev/flutter/bin/flutter precache"]
            )

    def delete_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            files.directory(
                path=f"{home}/dev/flutter",
                present=False
            )
