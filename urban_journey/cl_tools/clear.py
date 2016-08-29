import sys
from os.path import isdir, join

from .cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError, PluginsMissingError


class clear(ClBase):
    @staticmethod
    def description():
        return "Clears all plugins from this project"

    @staticmethod
    def usage():
        return "usage: uj clear"

    @staticmethod
    def main(args):
        try:
            uj_project = UjProject(verbosity=1)
        except InvalidUjProjectError as e:
            sys.exit(e.args[0])
        uj_project.clear()
