import re
from importlib import import_module
from pathlib import Path

for f in Path(__file__).parent.glob("./*/*.py"):
    module_name = f.stem
    if (not module_name.startswith("_")) and (module_name not in globals()):
        # NOTE: PREVENT IMPORTING __init__ and double module imports
        pathRegex = ".*(\/)(.+)(\/)(.+)$"
        module_path = re.sub(pathRegex, r'.\4', str(f.parent))
        import_module(f"{module_path}.{module_name}", __package__)
    del f, module_name

del import_module, Path
