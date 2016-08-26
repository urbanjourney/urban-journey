from .cl_base import ClBase
from urban_journey import UjProject
from urban_journey.uj_project import InvalidUjProjectError


class update(ClBase):
    @staticmethod
    def description():
        return "Update plugins to latest version."

    @staticmethod
    def usage():
        return "usage: uj update [-f|--force] [<plugins>]"

    @staticmethod
    def main(args: list):
        force = False
        if len(args):
            if "-f" in args:
                force = True
                args.pop(args.index("-f"))
            if "--force" in args:
                force = True
                args.pop(args.index("--force"))

        try:
            uj_project = UjProject()
        except InvalidUjProjectError:
            print("error: Not a uj project (or any of the parent directories)")
            return

        uj_project.update(*args, force=force)
