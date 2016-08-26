import os
from os import symlink
from os.path import join, isdir, isabs, isfile
from shutil import copyfile, move
import subprocess
import pickle
from collections import defaultdict
import pip

from urban_journey import __version__ as uj_version
from urban_journey.common.rm import rm

# Check whether git is available and import gitpython if it is.
try:
    subprocess.run(["git", "--version"], stdout=subprocess.PIPE)
    from git import Repo
    from git.exc import InvalidGitRepositoryError, RepositoryDirtyError, UnmergedEntriesError
    git_available = True
except OSError:
    git_available = False

empty_project_dir = os.path.join(os.path.dirname(__file__), "empty_project")


class InvalidUjProjectError(Exception):
    pass


class UjProject:
    def __init__(self, path=os.getcwd()):
        # Find project root folder
        self.path = self.find_project_root(os.path.abspath(path))
        if self.path is None:
            raise InvalidUjProjectError()

        # Load in project __init__ file.
        globs = {}
        with open(join(self.path, "__init__.py")) as f:
            exec(f.read(), globs)

        self.__dependencies = None
        self.__python_dependencies = None
        self.__version = globs.pop('__version__', None)
        self.__author = globs.pop('__author__', '')
        self.__dependencies_satisfied = False

        self.update_handlers = {
            "git": self.update_git,
            "symlink": self.update_symlink,
            "web": self.update_web,
            "zip": self.update_zip,
            "copy": self.update_copy,
        }

        self.load_dependency_list()

    @property
    def dependencies(self):
        return self.__dependencies

    @property
    def python_dependencies(self):
        return self.__python_dependencies

    @property
    def dependencies_satisfied(self):
        return self.__dependencies_satisfied

    def get_metadata(self):
        if isfile(join(self.path, ".uj", "dependency_metadata")):
            return pickle.load(open(join(self.path, ".uj", "dependency_metadata"), "rb"))
        else:
            return {}

    def set_metadata(self, value):
        pickle.dump(value, open(join(self.path, ".uj", "dependency_metadata"), "wb"))

    @property
    def version(self):
        return self.__version

    @property
    def author(self):
        return self.__author

    @staticmethod
    def init(path=None):
        """Creates an empty uj project. If possible and not existing, it initializes a git repository."""
        # Initialize current directory if no arguments where given.
        target_directory = path or "./"

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

    def update(self, *args, force=False):
        if len(args):
            for arg in args:
                if arg in self.dependencies:
                    self.update_dependency(arg, self.dependencies[arg], force)
                else:
                    print("WARNING: No dependency named '{}'".format(arg))
        else:
            while True:
                for name, sources in self.dependencies.items():
                    self.update_dependency(name, sources, force)
                if self.load_dependency_list():
                    return

    def load_dependency_list(self):
        """(Re)loads the list of dependencies. Returns True if all dependencies are satisfied."""
        # Load in project __init__ file.
        globs = {}
        with open(join(self.path, "__init__.py")) as f:
            exec(f.read(), globs)

        self.__dependencies = defaultdict(list, globs.pop('dependencies', {}))
        self.__python_dependencies = globs.pop('python_dependencies', [])

        # Get dependencies from dependencies.
        for entry in os.scandir(join(self.path, "dependencies")):
            if entry.is_dir():
                # Load in project __init__ file.
                d_project = UjProject(entry.path)
                for name, sources in d_project.dependencies.items():
                    for source in sources:
                        if source not in self.dependencies[name]:
                            self.dependencies[name].append(source)
                for pd in d_project.python_dependencies:
                    if pd not in self.python_dependencies:
                        self.python_dependencies.append(pd)

        # Print warning for missing python dependencies
        installed = [i.key for i in pip.get_installed_distributions()]
        for package in self.python_dependencies:
            if package not in installed:
                print("WARNING: Python package dependency '{}' missing.".format(package))

        # Check for unsatisfied dependencies.
        for name in self.dependencies:
            if not isdir(join(self.path, "dependencies", name)):
                self.__dependencies_satisfied = False
                return False
        self.__dependencies_satisfied = True
        return True

    def update_dependency(self, name, sources, force):
        dm = self.get_metadata()
        target_dir = join(self.path, "dependencies", name)

        # Try to use last used source.
        if name in dm and isdir(target_dir):
            if __name__ == '__main__':
                if self.update_handlers[dm[name][0]](name, dm[1]):
                    return True

        used_source = None
        # Last used source failed, try other sources
        for method, source in sources:
            if self.update_handlers[method](name, source, force):
                used_source = (method, source)
                break

        if used_source is None:
            print("Unable to update dependency '{}'.".format(name))
            return False

        # Working source found, saving source in dependancy metadata file.
        dm[name] = used_source
        self.set_metadata(dm)
        return True

    def run(self):
        pass

    def test(self):
        pass

    @staticmethod
    def find_project_root(path):
        if not isdir(path):
            return None
        prev_path = None
        while path != prev_path:
            if os.path.isdir(os.path.join(path, ".uj")):
                return path
            prev_path = path
            path = os.path.normpath(os.path.join(path, '..'))

    def find_local_extension_nodes(self):
        pass

    def find_external_extension_nodes(self):
        pass

    def check_dependencies(self):
        pass

    def is_valid(self):
        pass

    # Loads dependencies into project.
    def update_git(self, name, source, force):
        """Clone dependency from a git repository"""
        if git_available:
            target_dir = join(self.path, "dependencies", name)

            # Clone if the dependency doesn't exist or is being forced. Otherwise try pulling
            if not isdir(target_dir) or force:
                return self.git_clone(name, source)
            else:
                return self.git_pull(name, source)
        else:
            # No git os this computer.
            return False

    def git_clone(self, name, source):
        if git_available:
            target_dir = join(self.path, "dependencies", name)
            temp_dir = join(self.path, "dependencies", "temp_" + name)

            try:
                # Clone repository to temporary folder
                repo = Repo.clone_from(source, temp_dir)
            except:
                return False

            # Check if valid uj project.
            try:
                UjProject(temp_dir)
            except InvalidUjProjectError:
                return False

            # Delete old version of project if exiting
            rm(target_dir)

            # Move temp dir to target location and clean.
            move(temp_dir, target_dir)
            rm(temp_dir)
            return True
        else:
            return False

    def git_pull(self, name, source):
        target_dir = join(self.path, "dependencies", name)
        try:
            repo = Repo(target_dir)
            try:
                repo.remote().pull()
                return True
            except RepositoryDirtyError:
                print("WARNING: Repository for dependency '{}' is dirty.".format(name))
                return True
            except UnmergedEntriesError:
                print("WARNING: Repository for dependency '{}' has unmerged changes.".format(name))
                return True
        except InvalidGitRepositoryError:
            # This is an invalid git repository. Clone it.
            return self.git_clone(name, source)

    def update_symlink(self, name, source, force):
        """Create symlink to dependency"""
        target_dir = join(self.path, "dependencies", name)

        # Only update if the dependency doesn't exist or is being forced.
        if not force and isdir(target_dir):
            return True

        # If source dir path is relative, get absolute path relative to the project root.
        if not isabs(source):
            source = join(self.path, source)

        # Check if source dir exists.
        if not isdir(source):
            return False

        # Check if source dir is a valid uj project.
        try:
            UjProject(source)
        except InvalidUjProjectError:
            return False

        rm(target_dir)
        symlink(source, target_dir, target_is_directory=True)
        return True

    def update_web(self, name, source, force):
        """Download and extract zip file from the web"""
        raise NotImplementedError()

    def update_zip(self, name, source, force):
        """Extract local zip file."""
        raise NotImplementedError()

    def update_copy(self, name, source, force):
        """Copy dependency from local folder."""
        raise NotImplementedError()
