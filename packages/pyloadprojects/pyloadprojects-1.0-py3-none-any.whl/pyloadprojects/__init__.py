__version__ = "1.0"

import platform
from .plp import CreateL
from .data import *



def pyload(name: str,
           file: str,
           target: str,
           ):
    print(f"PyLoadProjects: {__version__}")
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}\n")

    create = CreateL(
        name, 
        file, 
        target
    )
