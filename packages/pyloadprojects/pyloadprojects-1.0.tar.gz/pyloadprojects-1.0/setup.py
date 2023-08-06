from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='pyloadprojects',
  version='1.0',
  author='AnKei',
  description='A simple installer of the program.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/AnKei-2022/PyLoadProjects',
  packages=find_packages(),
  install_requires=['elevate>=0.1.3', 'pywin32'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python',
  python_requires='>=3.8'
)
