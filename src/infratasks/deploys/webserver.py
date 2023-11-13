from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class WebserverDeployment(Deployment):
    name = "webserver"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = ["apt.mongodb", "apt.nginx", "apt.pgadmin4", "apt.apache2", "apt.dbeaver", "apt.ufw"]
