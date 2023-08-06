# PyLoadProjects
A simple installer of the program. Many probably know that it is possible to convert .py files to .exe, but what if the project includes not only modules and python files used.

```
pip install pyloadprojects
```
First you need to have a Zip folder with your finished project to copy. Import the module, specify the parameters in the pyload function.

```python
import pyloadprojects as plp


plp.pyload(
    "MyProgram", # project name
    "MyProgram.zip", # the path to the Zip folder
    "C:\\Program Files\\MyProgram\\MyProgram.exe" # the path to the executable file
)

```

And now a folder with the name of your project will be created in the current directory.

```python
import myprogram as mp

mp.install()
```

Import the module with the name of your project and run the "install" function.

## How does it work?
All your files need to be compressed into a ZIP file, then this file is copied and embedded in Python code. When you run the program, a ZIP file is created on your PC and extracted with your files.
