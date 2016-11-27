"""Command line tools"""

import sys
from urban_journey.cl_tools import cl_tools
from urban_journey import __version__ as uj_version


def main(args=sys.argv[1:]):
    """
    Main entry point for the uj command line command.

    :param args: Arguments passed int he command line.
    """

    # If no arguments where passed, print the help message.
    if len(args) < 1:
        display_help()
        return

    # If uj version was requested. Print it.
    if args[0] in ['-v', '--version']:
        print("uj version {}".format(uj_version))
        return

    # If the help message ws requested, print it.
    if args[0] in ['-h', '--help']:
        display_help()
        return

    # Check whether a valid cl_tools command was called.
    if args[0] in cl_tools:
        # If a parameter was passed and that parameter was a request for help. Print the command usage.
        if len(args) > 1:
            if args[1] in ['-h', '--help']:
                print(cl_tools[args[0]].usage())
                return
        # Else run the command.
        cl_tools[args[0]].main(args[1:])
    else:
        # If an unrecognised command was called print a error message.
        print("uj: '{}' is not a uj command. See 'uj --help'.".format(args[0]))


def display_help():
    """
    Prints the help message.
    """
    msg = """Urban Journey command line interface

usage: uj [-v|--version] [-h|--help] <command> [<args>]

{commands}

for command help: uj <command> -h

"""
    commands = ""
    for name, tool in cl_tools.items():
        commands += "   {:<10}   {}\n".format(name, tool.description())

    print(msg.format(commands=commands))


if __name__ == "__main__":
    main()
