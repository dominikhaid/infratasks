from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class DesktopDeployment(Deployment):
    name = "desktop"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = ["apt.lxde",
                             "apt.lightdm",
                             "apt.chrome",
                             "apt.gnome",
                             "apt.i3",
                             "apt.kodi",
                             "apt.obinskit",
                             "apt.apps",
                             "python.rofimoji",
                             "python.pywall",
                             ]
