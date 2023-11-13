from pyinfra.operations import server

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class JavaOperation(Operation, OpsUtil):
    name = "java"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        server.shell(
            name="Installing Gradle",
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk install gradle"],
            _shell_executable="bash"
        )

        server.shell(
            name="Installing Springboot",
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk install springboot"],
            _shell_executable="bash"
        )

        server.shell(
            name="Installing Groovy",
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk install groovy"],
            _shell_executable="bash"
        )

        server.shell(
            name="Installing Maven",
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk install maven"],
            _shell_executable="bash"
        )

        server.shell(
            name="Installing Java 11",
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk install java 11.0.2-open"],
            _shell_executable="bash"
        )

    def delete_debian_amd64(self):
        server.shell(
            name="Uninstalling {} with sdkman".format(self.name.title()),
            commands=["source $HOME/.sdkman/bin/sdkman-init.sh && sdk uninstall java"],
            _shell_executable="bash"
        )
        # TODO
