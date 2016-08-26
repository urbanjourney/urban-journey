from urban_journey.cl_tools.cl_base import ClBase
from urban_journey import UjProject


class init(ClBase):
    @staticmethod
    def description():
        return "Creates an empty uj project. If possible and not existing, it initializes a git repository."

    @staticmethod
    def usage():
        return "usage: uj init [<directory>]"

    @staticmethod
    def main(args):
        if len(args):
            UjProject.init(args[0])
        else:
            UjProject.init()
