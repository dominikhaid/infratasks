```Python
# Example deployment configurations
dpl = {"terminal": True}
dpl = {"terminal": True, "desktop": True}
dpl = {"terminal": False}
dpl = {"terminal": {"configure": True}}
dpl = {"terminal": {"configure": False}}
dpl = {"terminal": {"configure": True, "delete": True}}
dpl = {"terminal": {"configure": True, "delete": False}}
dpl = {"terminal": {"configure": False, "delete": False}}
dpl = {"terminal": {"configure": False, "delete": True}}
dpl = ["terminal"]
dpl = "terminal"

# Example operations configurations
ops = {"apt.fzf": True}
ops = {"apt.fzf": False}
ops = {"apt.fzf": {"configure": True}}
ops = {"apt.fzf": {"configure": False}}
ops = {"apt.fzf": {"configure": True, "delete": True}}
ops = {"apt.fzf": {"configure": True, "delete": False}}
ops = {"apt.fzf": {"configure": False, "delete": False}}
ops = {"apt.fzf": {"configure": False, "delete": True}}
ops = ["apt.fzf"]
ops = "apt.fzf"
ops = "cargo.broot"

# Include/Exclude single operations or deployments configurations
exclude = "fzf"
exclude = ["terminal", "fzf"]

include = "cargo.exa"
include = {"user.pyinfra": {"configure": True, "delete": False}}
include = ["terminal", "cargo.exa"]

configure = {"fzf": {"configure": False, "delete": True}}
configure = {"terminal": {"configure": False, "delete": False}}
```
