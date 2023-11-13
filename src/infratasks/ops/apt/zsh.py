from pyinfra.operations import server, git, files, apt

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class ZshOperation(Operation, AptUtil):
    name = "zsh"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        home = self.host_data["home"]
        user = self.host_data["user"]

        if home and user:
            apt.packages(
                name="Install {} Apt Packages".format(self.name.title()),
                packages=[self.name],
                update=self.should_apt_update(),
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
                present=True
            )

            server.shell(
                name="Remove Oh-My-Zsh",
                commands=[f"rm -rf {home}/.oh-my-zsh"],
            )
            server.shell(
                name="Install ZSH Tooling",
                commands=["curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | bash",
                          f"cd {home} && curl -L git.io/antigen > antigen.zsh"],
            )

            files.directory(
                path=f"{home}/dev/zsh-autocomplete",
                present=False,
                _on_success=self.auto_complete
            )

            passwd = self.apt_use_sudo_password()
            if isinstance(passwd, str):
                server.shell(
                    name="Setting ZSH as default shell",
                    commands=[f"echo {passwd} | chsh -s $(which zsh)"],
                )

    def auto_complete(self, state, stdout, stderr):
        home = self.host_data["home"]
        user = self.host_data["user"]

        if home and user:
            files.directory(
                path=f"{home}/dev/",
                user=f"{user}",
                group=f"{user}",
                present=True)

            git.repo(
                name="Clone Zsh AutoCoomplete",
                src="https://github.com/marlonrichert/zsh-autocomplete.git",
                dest=f"{home}/dev/zsh-autocomplete",
            )

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall {} Apt Packages".format(self.name.title()),
            packages=[self.name],
            present=False,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        home = self.host_data["home"]
        if home:
            server.shell(
                name="Remove Oh-My-Zsh",
                commands=[f"rm -rf {home}/.oh-my-zsh"],
            )

            files.directory(
                path=f"{home}/dev/zsh-autocomplete",
                present=False
            )
