import inspect
import pkgutil

from .basic_nodes import path as default_nodes_path

__all__ = ['update_extensions', 'extension_paths', 'node_register']

extension_paths = [default_nodes_path]

node_register = {}


def update_extensions():
    """Looks for nodes in the extension paths."""
    # This has to be imported here in order to avoid circular imports.
    from urban_journey.ujml.node_base import NodeBase

    # Iterate through all modules in the extension paths.
    for loader, module_name, is_pkg in pkgutil.iter_modules(extension_paths):
        module = loader.find_module(module_name).load_module(module_name)
        # Looping through all members of each module to find the module classes.
        for member_name, member in inspect.getmembers(module):
            # Ignore all private members
            if member_name.startswith('__'):
                continue
            # Add the member to the node register if it's a node.
            if isinstance(member, type):
                if issubclass(member, NodeBase):
                    node_register[member_name] = member
