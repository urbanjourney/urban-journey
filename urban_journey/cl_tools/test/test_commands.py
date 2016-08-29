import unittest
import os
from tempfile import mkdtemp
import subprocess
import shutil
import errno
import sys
from io import StringIO

from urban_journey.__main__ import main as uj_main
from urban_journey.uj_project import empty_project_dir, UjProject, InvalidUjProjectError

# Check whether git is available and import git python if it is.
try:
    subprocess.run(["git", "--version"], stdout=subprocess.PIPE)
    from git import Repo
    from git.exc import InvalidGitRepositoryError
    git_available = True
except OSError:
    git_available = False


def projects():
    test_dir = os.path.normpath(os.path.dirname(__file__))
    p_list = ['t1', 't2', 't3']
    for project_name in p_list:
        try:
            uj_project = UjProject(os.path.join(test_dir, project_name))
        except InvalidUjProjectError:
            raise Exception("If this error occurs it means the one or more of the urban journey test projects in"
                            "urban_journey/cl_tools/test have been corrupted and will have to be recreated."
                            "t1: Simple empty project."
                            "t2: Must include t1 as a symlink plugin. Optionally git from 'ssh://git@simvps.tk/git/trepo'"
                            "t3: Must include t2 as a symlink plugin. src/main.ujml must be"
                            "<?xml version='1.0'?>"
                            "<ujml version='0.0.1'>"
                            "  <data id='d1'>1234567890</data>"
                            "  <script>"
                            "    a = data['d1']"
                            "  </script>"
                            "</ujml>")
        yield uj_project


def clear_projects():
    for project in projects():
        project.clear()


class TestCommands(unittest.TestCase):
    def test_init(self):
        """Tests the init command"""
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

    def test_update_list(self):
        """Tests the update and list commands"""
        old_cwd = os.getcwd()
        clear_projects()

        t3_dir = os.path.join(os.path.normpath(os.path.dirname(__file__)), "t3")
        os.chdir(t3_dir)

        old_stdout = sys.stdout
        sys.stdout = std_out = StringIO()
        uj_main(["list"])
        sys.stdout = old_stdout
        # print("'''{}'''".format(std_out.getvalue()))
        assert '''plugins:
  t2 missing''' in std_out.getvalue()

        assert "Missing plugins, please update project to get node list" in std_out.getvalue()

        uj_main(["update"])

        sys.stdout = std_out = StringIO()
        uj_main(["list"])
        sys.stdout = old_stdout

        # Since the plugins and nodes are stored in simple dictionaries they can appear in any order. Which is why each
        # line is checked individually.
        assert "plugins:" in std_out.getvalue()
        assert "t1 present ['symlink', '../t1']" in std_out.getvalue()
        assert "t2 present ['symlink', '../t2']" in std_out.getvalue()

        assert "nodes:" in std_out.getvalue()
        assert "  t3_node" in std_out.getvalue()
        assert "  t1_node" in std_out.getvalue()
        assert "  t2_node" in std_out.getvalue()
        assert "  NodeBase" in std_out.getvalue()

        os.chdir(old_cwd)

    def test_run(self):
        clear_projects()

        t3_dir = os.path.join(os.path.normpath(os.path.dirname(__file__)), "t3")

        project = UjProject(t3_dir)
        project.update()

        project.run()
        assert os.path.isfile(os.path.join(t3_dir, ".uj", "plugin_symlinks", "works"))

