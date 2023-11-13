_su_shell = "bash"
infra_user_name = "infra"
infra_user_pw = "infra"

use_sudo = False
use_sudo_password = False

sys_use_sudo = True
sys_sudo_user = infra_user_name
sys_use_sudo_password = "example"
# sys_use_sudo_password = infra_user_pw

apt_use_sudo=True
apt_use_sudo_password = "example"
# apt_sudo_user = infra_user_name
# apt_use_sudo_password = infra_user_pw
# apt_use_sudo_password = True
# apt_update = ["fzf"]

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
