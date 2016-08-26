from urban_journey.cl_tools.cl_base import ClBase
from urban_journey import UjProject


class run(ClBase):
    @staticmethod
    def description():
        return "Load uj extensions and execute src/main.py:main(args)"

    @staticmethod
    def usage():
        return "usage: uj run"

    @staticmethod
    def main(args):
        print("Running run")
        project = UjProject()


def check_dependencies():
    pass


def load_dependencies():
    pass
