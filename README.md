# Pearun

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pearun)](https://pypi.org/project/pearun/)
[![PyPI](https://img.shields.io/pypi/v/pearun)](https://pypi.org/project/pearun/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pearun)](https://pypi.org/project/pearun/)
[![Build Status](https://travis-ci.com/Krakenus/Pearun.svg?branch=master)](https://travis-ci.com/Krakenus/Pearun)

A simple utility to run user defined commands.

Inspired by scripts in package.json of npm based projects.

## Install package

`pip install pearun`

## Usage

User commands are parsed from Pearunfile which contains simple json dictionary.

It is possible to run inline shell commands or execute whole script files.

With your Pearunfile ready, you can list your commands by: 

`pearun` or `pearun --help`

Or with `-f/--file` argument when your Pearunfile is not in your CWD:

`pearun -f <path_to_Pearunfile>` or `pearun --file <path_to_Pearunfile>`

To execute your command, simply type its name as an argument:

`pearun hello_world`

You can also append custom command line arguments after the command name:

`pearun script:default my_custom_args`


### Pearunfile example

```.json
{
    "hello_world": "echo \"Hello World!\"",
    "script:default": "./script.sh",
    "script:with_arg": "./script.sh some_arg",
    "boolean": "echo \"TRUE/FALSE\"",
    "pyth": "python -c \"print(1 + 1)\""
}
```

See examples folder to try this Pearunfile.
