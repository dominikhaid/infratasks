from pyinfra.operations import apt, git
from pyinfra.operations import files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class GitOperation(Operation, AptUtil):
    name = "git"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = [
        "git",
        "gh",
        "git-flow",
    ]

    def configure_debian_amd64(self):
        apt.key(
            name="Add the {} apt gpg key".format(self.name.title()),
            src="https://cli.github.com/packages/githubcli-archive-keyring.gpg",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user()
        )

        apt.packages(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            update=True,
            packages=self.packages,
            present=True,
        )

        git_opts = self.git_opts
        if git_opts:
            for key, val in git_opts.items():
                git.config(
                    name=key,
                    key=key,
                    value=val,
                )

    def delete_debian_amd64(self):
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=False,
        )

        home = self.host_data["home"]

        if home:
            files.file(
                name="Remove Home Git Config",
                path=f"{home}/.gitconfig",
                present=False
            )
