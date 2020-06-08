"""
WIDGETS
=======
"""

import importlib
import pkgutil

PATH = "mathsnuggets/widgets"
PREFIX = PATH.replace("/", ".") + "."
modules = [name for _, name, _ in pkgutil.iter_modules([PATH], PREFIX)]


def capitalize(string):
    """Gets class name from module name"""
    return "".join(map(str.title, string.split("_")))


info = {}

for name in modules:
    module = importlib.import_module(name)
    name = capitalize(name.split(".")[-1])
    cls = getattr(module, name)
    vars()[name] = cls
    info[name] = {
        "path": name,
        "name": cls.__doc__,
        "class": cls,
    }
    if hasattr(module, "test"):
        info[name]["test"] = module.test
