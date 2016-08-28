import sys
from os.path import isdir, join

from .cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError, PluginsMissingError


class list(ClBase):
    @staticmethod
    def description():
        return "Prints the list of plugins and plugins in this project."

    @staticmethod
    def usage():
        return "usage: uj list"

    @staticmethod
    def main(args):
        try:
            uj_project = UjProject()
        except InvalidUjProjectError as e:
            sys.exit(e.args[0])

        print("Project path: {}\n".format(uj_project.path))

        print("plugins:")
        for name in uj_project.plugins:
            try:
                UjProject(join(uj_project.path, "plugins", name))
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
            print("\nnodes:")
            for name in uj_project.nodes:
                print(" ", name)
        except PluginsMissingError:
            print("\nMissing plugins, please update project to get node list.")
