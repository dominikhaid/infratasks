from pyinfra.operations import server, git, files

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class Lz4Operation(Operation, OpsUtil):
    name = "lz4"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):

        home = self.host_data["home"]
        if home:
            files.directory(
                path=f"{home}/dev/zsh-autocomplete",
                present=False,
                _on_success=self.clone_and_install_debian_amd64
            )

    def clone_and_install_debian_amd64(self, state, stdout, stderr):
        home = self.host_data["home"]
        if home:
            git.repo(
                name="Clone {} Repo".format(self.name.title()),
                src="https://github.com/lz4/lz4",
                dest=f"{home}/dev/lz4",
            )

            server.shell(
                name=self.print_name(None, True),
                commands=[f"cd  {home}/dev/lz4 && make && make install",
                          f"cp  {home}/dev/lz4/lz4  {home}/go/bin/lz4"],
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                _sudo_user=self.use_sudo_user(),
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
