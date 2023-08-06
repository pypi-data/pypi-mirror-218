import os
from .data import *


class CreateL:

    def __init__(self,
                 name: str,
                 file: str,
                 target: str,
                 ):

        self.n = name
        self.f = file
        self.t = target

        with open(f"{name}.plp", "w") as fp:
            fp.write(f"NAME={name}\nFILE={file}\nTARGET={target}\n")
        print(f"Create Data file: {name}.plp")
        
        self.start()

    def start(self):
        self.create(type="dir", path=self.n.lower())
        self.create(
            type="file",
            path=f"{self.n.lower()}\\__init__.py",
            data_file=f"{self.n}.plp"
        )
        print(f"File processing: {self.f}")
        self.create(
            type="file",
            path=f"{self.n.lower()}\\bin.py",
            zip_file=self.f
        )

        print("Ready!")
    
    def create(self, **kwargs):

        if kwargs['type'] == "dir":
            if os.path.exists(kwargs["path"]):
                print(f"It is not possible to create a new {kwargs['path']} folder because a folder " +
                      "with that name already exists.")
                exit()
            else:
                os.mkdir(kwargs['path'])
        else:
            if "__init__.py" in kwargs['path']:
                data = get_inint(kwargs['data_file'])
            else:
                data = get_bin(kwargs['zip_file'])

            with open(kwargs['path'], "w") as f:
                f.write(data)
