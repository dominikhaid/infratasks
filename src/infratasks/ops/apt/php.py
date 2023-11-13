import os
import re

from pyinfra.operations import server, apt, files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class PhpOperation(Operation, AptUtil):
    name = "php"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]
    packages = ["php-dev",
                "unzip",
                "php-xdebug",
                "wget",
                "php-cli",
                "php-zip",
                "php8.2",
                "php8.2-zip",
                "php8.2-curl",
                "php8.2-mysql",
                "php8.2-pgsql",
                # "php8.2-fpm",
                "php8.2-mbstring",
                "php8.2-common"]

    def configure_debian_amd64(self):
        apt.key(
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            name="Add {} gpg Key".format(self.name.title()),
            src="https://packages.sury.org/php/apt.gpg",
        )

        lsb_info = self.host_data["lsb_release"]
        arch = re.sub(r'^\d\.\d\.\d-\d\d-', "", self.host_data["os_version"])
        linux_id = lsb_info["id"].lower()
        code_name = lsb_info["codename"]

        if os.path.isfile("/etc/apt/sources.list.d/php.list"):
            files.file(
                path="/etc/apt/sources.list.d/php.list",
                name=self.print_name("Remove Apt Source", False),
                _ignore_errors=True,
                present=False,
                _sudo=self.apt_use_sudo(),
                _use_sudo_password=self.apt_use_sudo_password(),
                _sudo_user=self.apt_use_sudo_user(),
            )

        apt.repo(
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src=(
                "deb [arch={}] https://packages.sury.org/php/"
                " {} main".format(arch, code_name)
            ),
            filename="{}".format(self.name),
            name="Add {} apt repo".format(self.name.title()),
        )

        apt.packages(
            name=self.print_name(None, True),
            update=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=self.packages,
            present=True,
        )
        # TODO FPM
        self.add_php_ini(self)
        self.install_composer(self)

    @staticmethod
    def add_php_ini(self):
        server.shell(
            name="Copy php.ini",
            commands=["cp /usr/lib/php/8.2/php.ini-development /etc/php/8.2/cli/php.ini",
                      "cp /usr/lib/php/8.2/php.ini-production /etc/php/8.2/cli/php-prod.ini"],
            _shell_executable="bash",
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

        server.shell(
            name="Add extension mbstring in php.ini",
            commands=[
                "sed -i 's/;extension=mbstring/extension=mbstring/g' /etc/php/8.2/cli/php.ini"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

        server.shell(
            name="Add extension curl in php.ini",
            commands=[
                "sed -i 's/;extension=curl/extension=curl/g' /etc/php/8.2/cli/php.ini"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

        server.shell(
            name="Add extension ftp in php.ini",
            commands=[
                "sed -i 's/;extension=ftp/extension=ftp/g' /etc/php/8.2/cli/php.ini"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

        server.shell(
            name="Add extension phar in php.ini",
            commands=[
                "sed -i 's/\\[PHP\\]/[PHP]\\n\\nextension = phar.so\\nsuhosin.executor.include.whitelist = phar/g' /etc/php/8.2/cli/php.ini"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

        server.shell(
            name="Add extension phar in php.ini",
            commands=[
                "sed -i 's/\\[PHP\\]/[PHP]\\n\\n[xdebug]\\nxdebug.mode=debug\\nxdebug.start_with_request=yes\\nxdebug.discover_client_host=1\\nxdebug.client_port=9003\\n/g' /etc/php/8.2/cli/php.ini"],
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
        )

    @staticmethod
    def install_composer(self):
        server.shell(
            name="Install Composer",
            commands=[
                "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer"],
            _shell_executable="bash",
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
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
                path=f"{home}/.local/bin/composer",
                name=self.print_name(None, False),
                _ignore_errors=True,
                _sudo=self.use_sudo(),
                _use_sudo_password=self.use_sudo_password(),
                present=False,
            )
