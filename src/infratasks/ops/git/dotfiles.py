from pyinfra.operations import git, files

from infratasks.utils.operations import Operation


class DotfilesOperation(Operation):
    name = "dotfiles"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    # TODO TMP PATH AND TEMPLATES
    @staticmethod
    def clean_up():
        files.directory(
            name="Ensure Dotfiles Repo is removed",
            path="/home/dominik/dev/dotfiles",
            present=False,
        )

    @staticmethod
    def clone_repo():
        git.repo(
            name="Clone Dotfiles",
            src="https://github.com/dominikhaid/dotfiles.git",
            dest="/home/dominik/dev/dotfiles",
        )

    def configure_debian_amd64(self):
        self.clean_up()
        self.clone_repo()
        files.directory(
            name="Ensure Install directory is present",
            path="/home/dominik/dev/",
            user="dominik",
            group="dominik",
            present=True,
        )

        files.directory(
            name="Make sure Linux dotfiles exit",
            path="/home/dominik/dev/dotfiles/linux",
        )

        files.directory(
            name="Make sure Linux dotfiles exit",
            path="/home/dominik/.config",
        )

        files.directory(
            name="Make sure Linux dotfiles exit",
            path="/home/dominik/dev"
        )

        files.rsync(
            name="Copy dotfiles",
            src="/home/dominik/dev/dotfiles/linux/config/*",
            dest="~/.config/"
        )

        files.rsync(
            name="Copy home files",
            src="/home/dominik/dev/dotfiles/linux/home/*",
            dest="~/"
        )

        files.rsync(
            name="Copy dev files",
            src="/home/dominik/dev/dotfiles/linux/scripts",
            dest="~/dev/"
        )

        files.rsync(
            name="Copy wallpaper",
            src="/home/dominik/dev/dotfiles/linux/wallpaper",
            dest="~/Bilder/"
        )

        files.directory(
            name="Ensure Dotfiles Repo is removed",
            path="/home/dominik/dev/dotfiles",
            present=False,
        )

    def delete_debian_amd64(self):
        files.directory(
            name="Ensure Dotfiles Repo is removed",
            path="/home/dominik/dev/dotfiles",
            present=False,
        )  # TODO
