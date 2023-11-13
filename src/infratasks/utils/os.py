from pyinfra.facts.server import Os, LinuxName, LsbRelease, Hostname, OsVersion, HasGui, Home, User


class OsUtil:
    def __init__(self, host):
        # self.arch = host.get_fact(Arch)
        # self.linux_distribution = host.get_fact(LinuxDistribution)
        self.linux_name = host.get_fact(LinuxName)
        self.os = host.get_fact(Os)
        self.os_version = host.get_fact(OsVersion)

        self.user = host.get_fact(User)
        self.hostname = host.get_fact(Hostname)
        self.lsb_release = host.get_fact(LsbRelease)
        self.has_gui = host.get_fact(HasGui)
        self.home = host.get_fact(Home)
        self.versions = host.data.get("version")
        self.git_opts = host.data.get("git_opts")

    def get_home(self) -> str:
        return self.home

    def get_os(self) -> str:
        return self.os

    def get_linux_name(self) -> str:
        return self.os

    def lsb_release(self) -> str:
        return self.lsb_release

    def get_host_data(self) -> dict[str, str]:
        return {
            # "arch": self.arch,
            # "linux_distribution": self.linux_distribution,
            "user": self.user,
            "os": self.os,
            "os_version": self.os_version,
            "linux_name": self.linux_name,
            "hostname": self.hostname,
            "home": self.home,
            "lsb_release": self.lsb_release,
            "has_gui": self.has_gui,
        }

    def get_versions(self) -> dict[str, str]:
        return self.versions

    def get_git_opts(self) -> dict[str, str]:
        return self.git_opts
