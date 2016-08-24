import os
from shutil import copyfile
import subprocess

from urban_journey.cl_tools.cl_base import ClBase
from urban_journey import __version__ as uj_version

empty_project_dir = os.path.join(os.path.dirname(__file__), "empty_project")

# Check whether git is available and import gitpython if it is.
try:
    subprocess.run(["git", "--version"], stdout=subprocess.PIPE)
    from git import Repo
    from git.exc import InvalidGitRepositoryError
    git_available = True
except OSError:
    git_available = False


class init(ClBase):
    @staticmethod
    def description():
        return "Creates an empty uj project. If possible and not existing, it initializes a git repository."

    @staticmethod
    def usage():
        return "usage: uj init [<directory>]"

    @staticmethod
    def main(args):
        # Initialize current directory if no arguments where given.
        target_directory = "./"
        if len(args):
            target_directory = args[0]

        # Walk through empty source directory and copy any non existing files.
        for (dir_path, dir_names, file_names) in os.walk(empty_project_dir):
            # Get relative path to source root.
            rel_path = os.path.relpath(dir_path, empty_project_dir)
            # Get path to current target directory
            target_path = os.path.normpath(os.path.join(target_directory, rel_path))
            # Create target directory if necessary.
            if not os.path.isdir(target_path):
                os.mkdir(target_path)
            # Create file id necessary.
            for file_name in file_names:
                if not os.path.exists(os.path.join(target_path, file_name)):
                    copyfile(os.path.join(dir_path, file_name), os.path.join(target_path, file_name))
                # If it's copying a ujml file. Fill is the version number.
                if file_name.endswith(".ujml"):
                    with open(os.path.join(target_path, file_name), "r") as f:
                        content = f.read()
                    with open(os.path.join(target_path, file_name), "w") as f:
                        f.write(content.format(version=uj_version))

        # If possible make sure it's a git repository.
        if git_available:
            try:
                Repo(target_directory)
            except InvalidGitRepositoryError:
                Repo.init(target_directory)


