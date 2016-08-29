import sys

from urban_journey.cl_tools.cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError


class run(ClBase):
    @staticmethod
    def description():
        return "Load uj plugins and execute src/main.py:main(args)"

    @staticmethod
    def usage():
        return "usage: uj run"

    @staticmethod
    def main(args):
        try:
            uj_project = UjProject(verbosity=1)
        except InvalidUjProjectError as e:
            sys.exit(e.args[0])

        uj_project.load_nodes()
        uj_project.run()


def check_plugins():
    pass


def load_plugins():
    pass
