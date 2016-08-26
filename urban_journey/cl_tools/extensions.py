from .cl_base import ClBase


class ext(ClBase):
    @staticmethod
    def description():
        return "Prints the list of extensions in this project."

    @staticmethod
    def usage():
        return "usage: uj ext"

    @staticmethod
    def main(args):
        pass
