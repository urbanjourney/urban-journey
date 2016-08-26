from .cl_base import ClBase


class test(ClBase):
    @staticmethod
    def description():
        return "Runs the unit tests in this project."

    @staticmethod
    def usage():
        return "usage: uj test"

    @staticmethod
    def main(args):
        pass
