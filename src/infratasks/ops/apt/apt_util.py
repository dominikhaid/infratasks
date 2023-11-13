from pyinfra import host

from infratasks.ops.ops_util import OpsUtil


class AptUtil(OpsUtil):
    name: str
    default_apt_args = {"sudo": True, "sudo_user": "infra"}

    def should_apt_update(self):
        update: list[str] = host.data.get("apt_update")
        return True if update and update.__contains__(self.name) else False

    @staticmethod
    def apt_use_sudo():
        sudo: dict[str, str] = host.data.get("apt_use_sudo")
        return True if sudo else False

    @staticmethod
    def apt_use_sudo_password():
        password: dict[str, str] = host.data.get("apt_use_sudo_password")
        return password if password is not None else True

    @staticmethod
    def apt_use_sudo_user():
        user: dict[str, str] = host.data.get("apt_sudo_user")
        return user if user else None
