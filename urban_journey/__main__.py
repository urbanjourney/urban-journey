"""Command line tools"""

import sys
from urban_journey.cl_tools import cl_tools
from urban_journey import __version__ as uj_version


def main(args=sys.argv[1:]):
    if len(args) < 1:
        display_help()
        return

    if args[0] in ['-v', '--version']:
        print("uj version {}".format(uj_version))
        return

    if args[0] in ['-h', '--help']:
        display_help()
        return

    if args[0] in cl_tools:
        if len(args) > 1:
            if args[1] in ['-h', '--help']:
                print(cl_tools[args[0]].usage())
                return
        cl_tools[args[0]].main(args[1:])
    else:
        print("uj: '{}' is not a uj command. See 'uj --help'.".format(args[0]))


def display_help():
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
