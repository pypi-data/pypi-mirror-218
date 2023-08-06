![Tipytools](tipy.png)

# Tipytools

 Tipytools is a Python library that simplifies the development of command-line tools by providing a collection of command-line tool templates and utilities. It offers features such as project setup, template-based file generation, logging, and integration with the fire library for creating user-friendly command-line interfaces.

## Features

- **Project setup made easy**: Use the `setup` command to quickly set up your project by initializing the environment and generating the project structure for your command-line tool.
- **Template-based project structure**: Tipytools provides a standardized project structure including essential files like README.md, setup.py, and template files for your tool's implementation.
- **Logging utility**: The library includes a logging module that allows easy printing of information, warnings, errors, and success messages with customizable colors.
- **Cross-platform compatibility**: Tipytools is designed to work seamlessly on Windows, Linux, and macOS, ensuring compatibility across different platforms.
- **Integration with fire library**: Tipytools integrates with the fire library to provide a user-friendly and intuitive command-line interface for your generated tools.
- **Optional virtual environment**: If you want to set up the project without a virtual environment, you can use the `maketool` command to generate only the folder structure without creating a virtual environment.

## Folder Structure

The folder structure for Tipytools is as follows:

```
Tipytools/
├── package_test/
│ └── test.py
├── [tool_name]/
│ ├── init.py
│ ├── [tool_name].py
│ └── logger.py
├── README.md
└── setup.py
```

## Installation:

```shell
pip install tipytool
```

You can install Tipytools directly from the GitHub repository:

```shell
pip install git+https://github.com/tipytools/tipytools.git
```

## Usage

1. Set up your project:
   - To create a virtual environment and generate the project structure, run the `setup` command and specify the tool name and optional virtual environment name.
   - Example: `tipy setup tool=[toolname] [optional: env=[venvname]]`
   - To generate only the folder structure without a virtual environment, run the `maketool` command and specify the tool name.
   - Example: `tipy maketool [toolname]`
2. Implement your tool's logic within the generated files and customize as needed.
3. Run your tool from the command line: Use the tool name followed by the desired command and arguments.
   - Example: `[toolname] [command] [arguments]`

During the project setup, Tipytools will initialize the environment by creating a virtual environment using the specified name (or a default name derived from the tool name). It will then generate the project structure, including the necessary files and directories. After the setup is complete, you can start implementing your tool's functionality within the provided template files.

Please refer to the [documentation](https://github.com/tipytools/tipytools) available in the repository for more detailed information, usage examples, and customization options.

Contributions, bug reports, and feature requests are welcome! Feel free to submit issues and pull requests on [GitHub](https://github.com/tipytools/tipytools) to help improve Tipytools.

- version: 1.0.0
- author: Mauly dotDev
