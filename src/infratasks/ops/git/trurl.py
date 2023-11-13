from pyinfra.operations import server, git, files, apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class TrurlOperation(Operation, AptUtil):
    name = "trurl"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = [
        "libcurl4-openssl-dev"
    ]

    def configure_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            apt.packages(
                name=self.print_name(None, True),
                _sudo=self.apt_use_sudo(),
                update=self.should_apt_update(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                present=True,
                packages=self.packages,
            )
            files.link(
                path=f"{home}/.local/bin/trurl",
                present=False
            )
            files.directory(
                path=f"{home}/.local/share/trurl",
                present=False,
                _on_success=self.make_trurl
            )

    def make_trurl(self, state, stdout, stderr):
        home = self.host_data["home"]
        git.repo(
            name=f"Clone {self.name.title()}",
            src="https://github.com/curl/trurl.git",
            dest=f"{home}/.local/share/trurl",
        )
        server.shell(
            name="Make {}".format(self.name.title()),
            commands=[
                f"cd {home}/.local/share/trurl && make",
                f"ln -s {home}/.local/share/trurl/trurl {home}/.local/bin/trurl",
            ],
            _shell_executable="bash"
        )

    def delete_debian_amd64(self):
        home = self.host_data["home"]
        if home:
            apt.packages(
                name=self.print_name(None, False),
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                present=False,
                packages=self.packages,
            )
            files.directory(
                path=f"{home}/.local/share/trurl",
                present=False
            )
            files.link(
                path=f"{home}/.local/bin/trurl",
                present=False
            )
