from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class SystemDeployment(Deployment):
    name = "system"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = ["apt.base", "apt.git", "apt.vnc", "apt.vagrant", "apt.ufw", "curl.webi", "apt.ufw"]
