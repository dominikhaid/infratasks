from pyinfra import host
from pyinfra.operations import systemd


class OpsUtil:
    name: str
    pkg: str

    def systemd(self, enable=True, running=True, restarted=False, title=None, service=None):
        if not title:
            title = self.name.title()
        if not service:
            service = self.name
        systemd.service(
            name=f"{title} enable:{enable} restart:{restarted} service:{service}",
            service=f"{service}.service",
            restarted=restarted,
            running=running,
            enabled=enable,
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
        )

    def systemd(self, enable=True, running=True, restarted=False, title=None, service=None):
        if not title:
            title = self.name.title()
        if not service:
            service = self.name
        systemd.service(
            name=f"{title} enable:{enable} restart:{restarted} service:{service}",
            service=f"{service}.service",
            restarted=restarted,
            running=running,
            enabled=enable,
            _sudo=self.use_sudo(),
            _use_sudo_password=self.use_sudo_password(),
            _sudo_user=self.use_sudo_user(),
        )

    def print_name(self, title: str | None = None, configure: bool = True) -> str:
        if not title:
            title = self.name.title()
        if not self.pkg:
            self.pkg = " "
        return f"Install {title} via {self.pkg.title()}" if configure else f"Uninstall {title}  via {self.pkg.title()}"

    @staticmethod
    def use_sudo():
        sudo: dict[str, str] = host.data.get("sys_use_sudo")
        return True if sudo else False

    @staticmethod
    def use_sudo_password():
        password: dict[str, str] = host.data.get("sys_use_sudo_password")
        return password if password is not None else True

    @staticmethod
    def use_sudo_user():
        user: dict[str, str] = host.data.get("sys_sudo_user")
        return user if user else None

    @staticmethod
    def get_version(command: str) -> str:
        name = command
        if not str or command.__len__() < 1:
            raise Exception("argument name missing")
        elif command == "go":
            command = "go version"
        elif command == "npm":
            command = "npm -v"
        else:
            command = f"{command} --version"

        status, stdout, stderr = host.run_shell_command(
            command=command,
        )
        if not status or name == "cargo" and not stdout[0].__contains__(name):
            raise Exception(f"please make sure {name} is installed, {name, command}")
        return stdout
