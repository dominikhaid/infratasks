from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class LanguagesDeployment(Deployment):
    name = "languages"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = [
        "apt.dotnet",
        "apt.lua",
        "apt.ruby",
        "curl.sdkman",
        "sdkman.java",
        "curl.rust",
        "curl.webi",
        "webi.node",
        "webi.go",
        "wget.flutter",
    ]
