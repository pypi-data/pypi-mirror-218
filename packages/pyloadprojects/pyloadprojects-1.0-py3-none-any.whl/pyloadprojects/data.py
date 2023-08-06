import base64


def get_bin(path) -> str:
    with open(path, "br") as f:
        bf = f.read()
        bf = base64.b64encode(bf)
    
    return f"zip_file = {bf}"


def get_inint(path) -> str:
    with open(path, "r", encoding="utf-8") as df:
        data_file = df.readlines()
    data = {}

    for parameter in data_file:
        if "=" in parameter:
            name = parameter.split("=")[0]
            num = parameter.split("=")[1]
            data[name.lower()] = num.strip("\n")
    wDr = "\\".join(data["target"].split("\\")[0:-1])
    
    INIT = f"""import os
import base64

from .bin import zip_file
from elevate import elevate
from zipfile import ZipFile
from win32com.client import Dispatch


elevate(show_console=False)

if os.path.exists("C:\\Program Files\\{data['name']}"):
    is_install = True
else:
    is_install = False

def install():
    def create_lnk(path: str, target: str, wDir: str):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.save()
    if not is_install:
        if not os.path.exists(f"{"{os.path.expanduser('~')}"}\\p.zip"):
            with open(f"{"{os.path.expanduser('~')}"}\\p.zip", "bw") as bf:
                bf.write(base64.b64decode(zip_file))

        z = ZipFile(f"{"{os.path.expanduser('~')}"}\\p.zip")
        os.mkdir(f"C:\\Program Files\\{data['name']}")
        z.extractall(f"C:\\Program Files\\{data['name']}")

        create_lnk(
            path=f"{"{os.path.expanduser('~')}"}\\Desktop\\{data['name']}.lnk",
            target=r"{data['target']}",
            wDir=r"{wDr}"
        )

        os.remove(f"{"{os.path.expanduser('~')}"}\\p.zip")
    else:
        return "The application is already on the computer."

    """
    
    return INIT
