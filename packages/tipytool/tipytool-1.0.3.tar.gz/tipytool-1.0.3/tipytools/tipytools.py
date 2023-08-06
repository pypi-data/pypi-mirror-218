import os
import sys
import fire
import subprocess
import tipytools.templates as tmp
from tipytools.logger import Log

CLUE = """Use the [maketool] command to generate the project structure
example: tipy maketool [toolname]"""

TOOL_NAME = ""


class Tipytools:
    def setup(self, *kwargs):
        """Set up a new project for a command-line tool.

        Args:
            tool_name (str): The name of the tool.
            env (str, optional): The name of the virtual environment. If not provided,
                a default environment name will be derived from the tool name.
        Usage:
            tipy setup <env> <tool>

        Examples:
            To set up a project for a tool named "mytool" with a virtual environment named "myenv", run:
            $ tipy setup tool=mytool env=myenv

            To set up a project for a tool named "mytool" without specifying a virtual environment, run:
            $ tipy setup tool=mytool
        """

        tool = ""
        env = ""

        Log('Setting up project, please wait...')

        for value in kwargs:
            if value.startswith("env="):
                env = value.split("=")[1]
            elif value.startswith("tool="):
                tool = value.split("=")[1]

        self.maketool(tool)

        if env == "":
            env = "{}-env".format(tool)
            self.init(env)

    def init(self, env):
        """Initialize the project and activate the virtual environment.

        Args:
            env (str): The name of the virtual environment.

        Usage:
            tipy init <env>

        Examples:
            To initialize the project with a virtual environment named "myenv", run:
            $ tipy init myenv
        """
        stdout = subprocess.run(["python", "-m", "venv", env])

        if stdout.returncode == 1:
            Log(stdout, "error")
        else:
            Log(CLUE)
            Log('Setup complete, happy hacking!', 'success')

            _type = sys.platform
            env_path = os.path.join(env, "Scripts", "activate")

            if _type.startswith("win"):
                subprocess.Popen(["cmd", "/k", env_path], shell=True).wait()
            elif _type.startswith("linux"):
                subprocess.Popen(["source", env_path], shell=True).wait()
            elif _type.startswith("darwin"):
                subprocess.Popen(["source", env_path], shell=True).wait()

        subprocess.run(["pip", "install", "fire"], shell=True)

    def maketool(self, tool_name):
        """Generate the folder structure for a new tool.

        Args:
            tool_name (str): The name of the tool.

        Usage:
            tipy maketool <tool_name>

        Examples:
            To generate the folder structure for a tool named "mytool", run:
            $ tipy maketool mytool
        """
        global TOOL_NAME
        TOOL_NAME = tool_name

        structure = {
            "tool_test/": {"placeholder": ""},
            f"{tool_name}/": {
                "__init__.py": "",
                f"{tool_name}.py": tmp.PACKAGE.replace('/toolname/', tool_name),
                'logger.py': tmp.LOGGER
            },
            "README.md": tmp.README,
            "setup": tmp.SETUP,
            "pyproject.toml": tmp.PYPROJECT_TOML,
        }

        if not os.path.exists(tool_name):
            for key, value in structure.items():
                if key.endswith("/"):
                    os.makedirs(key)
                    for _dir, content in value.items():
                        with open(f"{key}/{_dir}", "w", encoding="utf-8") as file:
                            file.write(content)
                else:
                    with open(key, "w", encoding="utf-8") as new_file:
                        new_file.write(value)


def main():
    fire.Fire(Tipytools)


if __name__ == "__main__":
    main()
