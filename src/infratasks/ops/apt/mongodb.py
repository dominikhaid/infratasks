import re

from pyinfra.operations import apt
from pyinfra.operations import files

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class MongodbOperation(Operation, AptUtil):
    name = "mongod"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        mongo_version = self.version.get("mongodb")
        if not mongo_version:
            raise Exception("dive version not found, please see help for more details")
        apt.deb(
            name=self.print_name(None, True),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src="https://downloads.mongodb.com/compass/mongodb-compass_{}_amd64.deb".format(mongo_version),
        )

        apt.key(
            name="Add the Mongo DB apt gpg key if we need to",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src="https://pgp.mongodb.com/server-7.0.asc",
        )

        lsb_info = self.host_data["lsb_release"]
        arch = re.sub(r'^\d\.\d\.\d-\d\d-', "", self.host_data["os_version"])
        code_name = lsb_info["codename"]

        apt.repo(
            name="Add the MongoDB repo",
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            src=(
                "deb [arch={}] http://repo.mongodb.org/apt/debian {}/mongodb-org/7.0 main".format(arch, code_name)
            ),
            filename="{}".format(self.name),
        )

        apt.packages(
            name=self.print_name(None, True),
            update=True,
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=["mongodb-org"],
            present=True,
            # _on_success=self.check_docker_works
        )

        self.systemd(True, True, True, "mongod", "mongod")

    def delete_debian_amd64(self):
        self.systemd(False, False, False, "mongod", "mongod")
        apt.packages(
            name=self.print_name(None, False),
            _sudo=self.apt_use_sudo(),
            _use_sudo_password=self.apt_use_sudo_password(),
            _sudo_user=self.apt_use_sudo_user(),
            packages=["mongodb-compass", "mongodb-org"],
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
