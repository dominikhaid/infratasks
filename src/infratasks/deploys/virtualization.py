from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class VirtualizationDeployment(Deployment):
    name = "virtualization"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = ["apt.qemu", "apt.vagrant"]
