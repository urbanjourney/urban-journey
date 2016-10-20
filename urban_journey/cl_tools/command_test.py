import sys

from urban_journey.cl_tools.cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError


class test(ClBase):
    """
    TODO: Give it the option to run a specific set of tests.
    """
    @staticmethod
    def description():
        return "Runs all unit tests in this project."

    @staticmethod
    def usage():
        return "usage: uj test"

    @staticmethod
    def main(args):
        verbosity = 2 if "-v" in args else 1

        try:
            uj_project = UjProject(verbosity=1)
        except InvalidUjProjectError as e:
            sys.exit(e.args[0])

        uj_project.load_nodes()
        uj_project.test(verbosity=verbosity)
        pass
