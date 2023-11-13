from infratasks.utils.deployments import Deployment
from infratasks.utils.operations import Operation


class TerminalDeployment(Deployment):
    name = "terminal"
    state = ""
    configure: bool
    configured: bool = False
    delete: bool
    deleted: bool = False
    operations: Operation = [
        "apt.fzf",
        "apt.zsh",
        "apt.neomutt",
        "apt.taskwarrior",
        "apt.ueberzug",
        "cargo.astree",
        "cargo.bottom",
        "cargo.broot",
        "cargo.exa",
        "cargo.gitui",
        "cargo.grex",
        "cargo.jq",
        "cargo.jsondiff",
        "cargo.just",
        "cargo.navi",
        "cargo.procs",
        "cargo.sd",
        "cargo.tailspin",
        "cargo.dust",
        "cargo.viu",
        "cargo.projectable",
        "cargo.zoxide",
        "cargo.yazi",
        "git.trurl",
        "go.lz4",
        "git.dasel",
        "git.yq",
        "go.lazygit",
        "go.lazydocker",
        "go.glow",
        "go.cs",
        "go.xc",
        "python.rofimoji",
        "curl.chtsh",
        "curl.webi",
        "npm.inshellisense",
        "webi.fd",
        "webi.rclone",
        "webi.rg",
        "curl.starship"
    ]
