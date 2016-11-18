import sys
from os.path import isdir, join

from .cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError, PluginsMissingError


class list(ClBase):
    @staticmethod
    def description():
        return "Prints the list of plugins and nodes in this project."

    @staticmethod
    def usage():
        return "usage: uj list [-t|--include-tests]"

    @staticmethod
    def main(args):
        include_tests = ('-t' in args) or ("--test" in args)

        try:
            uj_project = UjProject(verbosity=1,
                                   istest=include_tests)
        except InvalidUjProjectError as e:
            sys.exit(e.args[0])

        print("Project path: {}\n".format(uj_project.path))
        print("plugins:")
        for name in uj_project.plugins:
            try:
                UjProject(join(uj_project.path, "plugins", name),
                          istest=include_tests)
                if name in uj_project.get_metadata():
                    source = uj_project.get_metadata()[name]
                else:
                    source = ''
                present = "present"
            except InvalidUjProjectError:
                present = "missing"
                source = ""

            print(" ", name, present, source)

        try:
            uj_project.load_nodes()
            print("\nnodes (including tests)" if include_tests else "\nnodes:")
            for name in uj_project.nodes:
                print(" ", name)
        except PluginsMissingError:
            print("\nMissing plugins, please update project to get node list.")
