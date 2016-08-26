import os
from os import symlink, mkdir
from os.path import join, isdir, isabs, isfile, relpath
from shutil import copyfile, move
import subprocess
import pickle
from collections import defaultdict
import pip

from urban_journey import __version__ as uj_version, NodeBase
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
    def __init__(self, path=os.getcwd(), is_plugin=False):
        # Find project root folder
        self.path = self.find_project_root(os.path.abspath(path))
        self.is_plugin = is_plugin

        if self.path is None:
            raise InvalidUjProjectError()

        # Load in project __init__ file.
        globs = {}
        with open(join(self.path, "__init__.py")) as f:
            exec(f.read(), globs)

        self.__plugins = None
        self.__python_dependencies = None
        self.__version = None
        self.__author = ""
        self.__plugins_satisfied = False
        self.__nodes = None

        self.update_handlers = {
            "git": self.update_git,
            "symlink": self.update_symlink,
            "web": self.update_web,
            "zip": self.update_zip,
            "copy": self.update_copy,
        }

        # Create plugins folder if it doesn't exist.
        if not isdir(join(self.path, "plugins")):
            mkdir(join(self.path, "plugins"))

        # Create plugins/.gitignore if it doesn't exist.
        if not isfile(join(self.path, "plugins", ".gitignore")):
            with open(join(self.path, "plugins", ".gitignore"), "w") as f:
                f.write("*\n!.gitignore")

        self.load_project()

    @property
    def plugins(self):
        return self.__plugins

    @property
    def python_dependencies(self):
        return self.__python_dependencies

    @property
    def nodes(self):
        return self.__nodes
    @property
    def plugins_satisfied(self):
        return self.__plugins_satisfied

    def get_metadata(self):
        if isfile(join(self.path, ".uj", "plugin_metadata")):
            return pickle.load(open(join(self.path, ".uj", "plugin_metadata"), "rb"))
        else:
            return {}

    def set_metadata(self, value):
        pickle.dump(value, open(join(self.path, ".uj", "plugin_metadata"), "wb"))

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

    def load_project(self):
        """(Re)loads the project. Returns True if all plugins are satisfied."""
        # Load in project __init__ file.
        globs = {}
        with open(join(self.path, "__init__.py")) as f:
            exec(f.read(), globs)

        self.__plugins = defaultdict(list, globs.pop('plugins', {}))
        self.__python_dependencies = globs.pop('python_dependencies', [])
        self.__version = globs.pop('__version__', None)
        self.__author = globs.pop('__author__', '')

        self.__nodes = {}
        for name, obj in globs.items():
            if isinstance(obj, type):
                if issubclass(obj, NodeBase):
                    self.__nodes[name] = obj

        if not self.is_plugin:
            # Get plugins from plugins.
            for entry in os.scandir(join(self.path, "plugins")):
                if entry.is_dir():
                    # Load in project __init__ file.
                    d_project = UjProject(entry.path, True)
                    for name, sources in d_project.plugins.items():
                        for source in sources:
                            if source not in self.plugins[name]:
                                self.plugins[name].append(source)
                    for pd in d_project.python_dependencies:
                        if pd not in self.python_dependencies:
                            self.python_dependencies.append(pd)
                    for name, node in d_project.nodes.items():
                        if name not in self.nodes:
                            self.nodes[name] = node

        # Print warning for missing python plugins
        installed = [i.key for i in pip.get_installed_distributions()]
        for package in self.python_dependencies:
            if package not in installed:
                print("WARNING: Python package dependency '{}' missing.".format(package))

        # Check for unsatisfied plugins.
        for name in self.plugins:
            if not isdir(join(self.path, "plugins", name)):
                self.__plugins_satisfied = False
                return False
        self.__plugins_satisfied = True
        return True

    def update(self, *args, force=False):
        if len(args):
            for arg in args:
                if arg in self.plugins:
                    self.update_plugin(arg, self.plugins[arg], force)
                else:
                    print("WARNING: No plugin named '{}'".format(arg))
        else:
            while True:
                for name, sources in self.plugins.items():
                    self.update_plugin(name, sources, force)
                if self.load_project():
                    return

    def update_plugin(self, name, sources, force):
        dm = self.get_metadata()
        target_dir = join(self.path, "plugins", name)

        # Try to use last used source.
        if name in dm and isdir(target_dir):
            if self.update_handlers[dm[name][0]](name, dm[name][1], force):
                return True

        # Last used source failed, try other sources
        for method, source in sources:
            if self.update_handlers[method](name, source, force):
                dm[name] = (method, source)
                self.set_metadata(dm)
                return True

        print("Unable to update plugin '{}'.".format(name))
        return False

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

    def find_local_plugin_nodes(self):
        pass

    def find_external_plugin_nodes(self):
        pass

    def check_plugins(self):
        pass

    def is_valid(self):
        pass

    # Loads plugins into project.
    def update_git(self, name, source, force):
        """Clone plugin from a git repository"""
        if git_available:
            target_dir = join(self.path, "plugins", name)

            # Clone if the plugin doesn't exist or is being forced. Otherwise try pulling
            if not isdir(target_dir) or force:
                return self.git_clone(name, source)
            else:
                return self.git_pull(name, source)
        else:
            # No git os this computer.
            return False

    def git_clone(self, name, source):
        if git_available:
            target_dir = join(self.path, "plugins", name)
            temp_dir = join(self.path, "plugins", "temp_" + name)

            try:
                # Clone repository to temporary folder
                repo = Repo.clone_from(source, temp_dir)
                print("cloned '{}' from '{}'".format(name, source))
            except:
                return False

            # Check if valid uj project.
            try:
                UjProject(temp_dir, True)
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
        target_dir = join(self.path, "plugins", name)
        try:
            repo = Repo(target_dir)
            try:
                repo.remote().pull()
                print("pulled '{}' from '{}'".format(name, source))
                return True
            except RepositoryDirtyError:
                print("WARNING: Repository for plugin '{}' is dirty.".format(name))
                return True
            except UnmergedEntriesError:
                print("WARNING: Repository for plugin '{}' has unmerged changes.".format(name))
                return True
        except InvalidGitRepositoryError:
            # This is an invalid git repository. Clone it.
            return self.git_clone(name, source)

    def update_symlink(self, name, source, force):
        """Create symlink to plugin"""
        target_dir = join(self.path, "plugins", name)

        # Only update if the plugin doesn't exist or is being forced.
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
            UjProject(source, True)
        except InvalidUjProjectError:
            return False

        rm(target_dir)

        symlink(relpath(source, join(self.path, "plugins")), target_dir, target_is_directory=True)
        print("created symlink '{}' with source '{}'".format(name, target_dir))
        return True

    def update_web(self, name, source, force):
        """Download and extract zip file from the web"""
        raise NotImplementedError()

    def update_zip(self, name, source, force):
        """Extract local zip file."""
        raise NotImplementedError()

    def update_copy(self, name, source, force):
        """Copy plugin from local folder."""
        raise NotImplementedError()
