import re

from pyinfra.operations import apt
from pyinfra.operations import files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class Pgadmin4Operation(Operation, AptUtil):
    name = "pgadmin4"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        lsb_info = self.host_data["lsb_release"]
        arch = re.sub(r'^\d\.\d\.\d-\d\d-', "", self.host_data["os_version"])
        linux_id = lsb_info["id"].lower()
        code_name = lsb_info["codename"]

        apt.key(
            name="Add the {} gpg Key".format(self.name.title()),
            src="https://www.pgadmin.org/static/packages_pgadmin_org.pub",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
        )

        apt.repo(
            name="Add {} apt repo".format(self.name.title()),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src=(
                "deb [arch={}] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/{} "
                "{}  main".format(arch, code_name, self.name)
            ),
            filename=f"{self.name}",
        )

        apt.packages(
            name="Install {} Apt Packages".format(self.name.title()),
            packages=["pgadmin4-web"],
            update=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=True,
        )

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall {} Apt Packages".format(self.name.title()),
            packages=["pgadmin4-web"],
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
        )

        files.file(
            name="Remove {} from sources".format(self.name),
            path="/etc/apt/sources.list.d/{}.list".format(self.name),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            present=False,
        )

    # TODO execute post install /usr/pgadmin4/bin/setup-web.sh  email/pass/y/y
