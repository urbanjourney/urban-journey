import unittest
import os
from tempfile import mkdtemp
import subprocess
import shutil
import errno

from urban_journey.__main__ import main as uj_main
from urban_journey.cl_tools.init import empty_project_dir

# Check whether git is available and import git python if it is.
try:
    subprocess.run(["git", "--version"], stdout=subprocess.PIPE)
    from git import Repo
    from git.exc import InvalidGitRepositoryError
    git_available = True
except OSError:
    git_available = False


class TestInit(unittest.TestCase):
    def test_init(self):
        tmp_dir = mkdtemp()

        uj_main(["init", tmp_dir])

        # Walk through empty source directory and copy any non existing files.
        for (dir_path, dir_names, file_names) in os.walk(empty_project_dir):
            # Get relative path to source root.
            rel_path = os.path.relpath(dir_path, empty_project_dir)

            # Get path to current target directory
            target_path = os.path.normpath(os.path.join(tmp_dir, rel_path))

            # Check if the directory exists
            assert os.path.isdir(target_path)

            # Check if all files in the directory exist.
            for file_name in file_names:
                assert os.path.exists(os.path.join(target_path, file_name))

        if git_available:
            try:
                repo = Repo(tmp_dir)
            except InvalidGitRepositoryError:
                assert False

        try:
            shutil.rmtree(tmp_dir)  # delete directory
        except OSError as exc:
            if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                raise  # re-raise exception
