from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class DockerDeployment(Deployment):
    name = "docker"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = ["apt.dive", "apt.docker", "apt.rancher", "webi.k9s", "go.lazydocker"]
