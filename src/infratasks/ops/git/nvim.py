from pyinfra.operations import server, git, files

from infratasks.ops.ops_util import OpsUtil
from infratasks.utils.operations import Operation


class NvimOperation(Operation, OpsUtil):
    name = "neovim"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        files.directory(
            path="/home/dominik/.local/share/nvim",
            present=False
        )

        git.repo(
            name="Clone Nvim",
            src="https://github.com/neovim/neovim.git",
            dest="/home/dominik/.local/share/nvim",
        )

        server.shell(
            name="Make Nvim",
            commands=[
                "cd /home/dominik/.local/share/nvim && make CMAKE_BUILD_TYPE=\"RelWithDebInfo\" CMAKE_EXTRA_FLAGS=\"-DCMAKE_install=/home/dominik/.local/share/nvim\"",
                "cd /home/dominik/.local/share/nvim && make install",
                "ln -s /home/dominik/.local/share/nvim/bin/nvim /home/dominik/.local/bin/nvim",
            ],
            _shell_executable="bash"
        )

        files.directory(
            path="/home/dominik/.local/share/nvim/site/pack/packer/start/packer.nvim",
            present=False
        )

        git.repo(
            name="Clone Packer",
            src="https://github.com/wbthomason/packer.nvim",
            dest="/home/dominik/.local/share/nvim/site/pack/packer/start/packer.nvim",
        )

        files.directory(
            path="/home/dominik/.local/share/nvim/site/pack/packer/start/nvim-lspinstall",
            present=False
        )

        git.repo(
            name="Clone Lsp-Install",
            src="https://github.com/kabouzeid/nvim-lspinstall",
            dest="/home/dominik/.local/share/nvim/site/pack/packer/start/nvim-lspinstall",
        )

        server.shell(
            name="Downloading Pathogen",
            commands=["cd && curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim"],
            _shell_executable="bash"
        )

        server.shell(
            name="Install pynvim trough pipx",
            commands=["pipx install pynvim"],
            _shell_executable="bash"
        )

    def delete_debian_amd64(self):
        pass
        # TODO
    # if host.get_fact(LinuxName) == "Debian":

    # TODO TEMPLATES
    #   mkdir -p $USER_HOME/.vim/pack/themes/start

    #  git clone https://github.com/dirkvdb/ffmpegthumbnailer.git $USER_HOME/dev/ffmpegthumbnailer
    # cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_GIO=ON -DENABLE_THUMBNAILER=ON .
    #  make
    #  sudo  make install

    # git clone https://github.com/sdushantha/fontpreview  $USER_HOME/dev/fontpreview && cd $USER_HOME/dev/fontpreview && sudo make install
    # ln -s $USER_HOME/dev/fontpreview/fontpreview $USER_HOME/.local/bin/fontpreview
