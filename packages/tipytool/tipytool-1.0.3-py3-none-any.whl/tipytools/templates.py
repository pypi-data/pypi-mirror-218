PACKAGE = \
"""
import os
import sys
import fire
import subprocess
from /toolname/.logger import Log

def main():
    fire.Fire(Toolname)

class Toolname:

    def ur_command(self, param):
        ...
    
    
    def test(self):
        print('test method')
        ...


if __name__ == '__main__':
    main()
"""


SETUP =\
    """from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tool_name',
    version='1.0.0',
    author='Your Name',
    author_email='your@gmail.com',
    description='short synopsis of your tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tipytools/tipytools',
    py_modules=['tool_name.tool_name'], # example: ['tipytools.tipytools']
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'fire',
        # Add any other dependencies required by your tool
    ],
    entry_points='''
        [console_scripts]
        # tipy=tipytools.tipytools:main
        tool_name=tool_name.tool_name:main
    ''',
)
"""


README =\
    """# Tool name


```shell

```

- author: Your Name
- version: 1.0.0
"""


LOGGER =\
"""from typing import Optional


class Log:
    def __init__(self, param: str, type: Optional[str] = None):
        if type in [None, 'info']:
            print('\\n\\033[34mℹ', param, '\\033[0m')  # Blue color for info
            ...
        elif type == 'warning':
            print('\\n\\033[33m⚠', param, '\\033[0m')  # Yellow color for warning
            ...
        elif type == 'error':
            exit('\\n\\033[31m❌', param, '\\033[0m')  # Red color for error
            ...
        elif type == 'success':
            print('\\n\\033[32m✓', param, '\\033[0m')  # Green color for success
            ...
        else:
            exit("invalid log type: [ {} ]".format(type))
            ...
"""

PYPROJECT_TOML =\
"""[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "/toolname/"
authors = [{ name = "Your Name", email = "youremail@example.com" }]
description = "description of your tool"
readme = "README.md"
requires-python = ">=3.7"
keywords = [
    "command-line interface",
    "development tools",
    "Python library",
    "CLI utilities",
    "project scaffolding",
    "automation",
    "code generation",
    "tooling",
    "software development",
    "command-line applications"
]
license = { text = "BSD-3-Clause" }
classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
]
dependencies = ["fire"]
dynamic = ["version"]

[project.scripts]
my-script = "my_package.module:main"
"""