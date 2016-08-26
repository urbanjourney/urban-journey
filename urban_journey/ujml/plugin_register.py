import inspect
import pkgutil

from .basic_nodes import path as default_nodes_path

__all__ = ['update_plugins', 'plugin_paths', 'node_register']

plugin_paths = [default_nodes_path]

node_register = {}


def update_plugins():
    """Looks for nodes in the plugin paths."""
    # This has to be imported here in order to avoid circular imports.
    from urban_journey.ujml.node_base import NodeBase

    # Iterate through all modules in the plugin paths.
    for loader, module_name, is_pkg in pkgutil.iter_modules(plugin_paths):
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
