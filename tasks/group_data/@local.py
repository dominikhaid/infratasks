_su_shell = "bash"
infra_user_name = "infra"
infra_user_pw = "infra"

use_sudo = False
use_sudo_password = False

sys_use_sudo = True
sys_sudo_user = infra_user_name
sys_use_sudo_password = "dom53361."
# sys_use_sudo_password = infra_user_pw

apt_use_sudo=True
apt_use_sudo_password = "dom53361."
git_opts = {
    "user.name": "username",
    "user.email": "example@user.com",
    "core.pager": "delta",
    "url.\"git@github.com/\".insteadOf": "https://git@github.com/",
    "interactive.diffFilter": "delta --color-only",
    "delta.navigate": "true",
    "delta.line-numbers": "true",
    "merge.conflictstyle": "diff3",
    "diff.colorMoved": "zebra",
    "pull.rebase": "true",
    "fetch.prune": "true",
}


#dpl = {"system": True}
#dpl = {"system":True,"docker": True, "languages":True, "desktop":True}
#dpl = {"desktop":True}
#dpl = {"languages":True, "desktop":True}
ops = {"appimage.appimages": True}
#exclude = ["apache2", "nginx"]
