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


for name in modules:
    module = importlib.import_module(name)
    name = capitalize(name.split(".")[-1])
    vars()[name] = getattr(module, name)
