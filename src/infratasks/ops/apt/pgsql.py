from pyinfra import host
from pyinfra.facts.server import LsbRelease
from pyinfra.operations import apt, postgresql

from infratasks.ops.apt.apt_util import AptUtil
from infratasks.utils.operations import Operation


class PsqlOperation(Operation, AptUtil):
    name = "psql"
    configure = True
    delete = False
    candidates: list[dict[str, str]] = [{"os": "Linux", "linux_name": "Debian", "os_version": "amd64"}]

    def configure_debian_amd64(self):
        lsb_info = host.get_fact(LsbRelease)
        apt.key(
            name="Add the {} gpg Key".format(self.name.title()),
            src="https://www.postgresql.org/media/keys/ACCC4CF8.asc",
            _sudo=True
        )

        apt.repo(
            name="Add {} apt repo".format(self.name.title()),
            src=(
                "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt/ {}-pgdg main".format(lsb_info),
            ),
            filename="pgdg",
        )

        apt.packages(
            name="Install {} Apt Packages".format(lsb_info),
            packages=["postgresql"],
            update=True,
            peresent=True,
            _sudo=True
        )
        self.add_pgsql_user()

    def add_pgsql_user(self):
        psql_root_pw = "1234"
        postgresql.sql(
            name="Change PSQL root password",
            sql="ALTER USER postgres WITH PASSWORD '{}';".format(psql_root_pw),
            psql_user="psql",
        )

        psql_default_user = "default"
        postgresql.sql(
            name="Create {} User".format(psql_default_user),
            sql="CREATE USER {} with CREATEDB CREATEROLE;".format(psql_default_user),
            psql_user="psql",
        )

        psql_default_user_pw = "default"
        postgresql.sql(
            name="Change {} user password",
            sql="ALTER USER {} with PASSWORD '{}';".format(psql_default_user, psql_default_user_pw),
            psql_user="psql",
        )

        # TODO Test sudo systemctl is-enabled postgresql sudo systemctl status postgresql global variables

    def delete_debian_amd64(self):
        apt.packages(
            name="Uninstall {} Apt Packages".format(self.name.title()),
            packages=["postgresql"],
            present=False,
            _sudo=True
        )
