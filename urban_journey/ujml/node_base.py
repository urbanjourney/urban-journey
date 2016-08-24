import os
import inspect

from lxml import etree

from urban_journey.common.cached import cached
from urban_journey.ujml.register import node_register, update_extensions
from urban_journey.ujml.exceptions import UnknownElementError, IdNotFoundError
from urban_journey.ujml.attributes import String, Data


class NodeBase:
    id = String(optional_value=None)

    def __init__(self, element: etree.ElementBase, root):
        element.node = self
        self.element = element
        self.parents = []
        self.__children = None
        self.__file_name = None
        self.__root = root
        self.root.register_node(self)

    def __del__(self):
        self.root.deregister_node(self)
        map(self.remove_parent, self.parents)
        if self.__children is not None:
            map(self.remove_child, self.__children)

    @cached
    def tag(self):
        return self.element.tag

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
            parent.add_child(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.add_parent(self)

    def remove_parent(self, parent):
        if parent in self.parents:
            self.parents.remove(parent)
            parent.remove_child(self)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.remove_parent(self)

    def find_node_by_id(self, node_id):
        if node_id in self.root.node_dict_by_id:
            return self.root.node_dict_by_id[node_id]

    @property
    def root(self):
        return self.__root

    @cached
    def file_name(self):
        return self.root.file_name

    @cached
    def source_line(self):
        return self.element.sourceline

    def exec(self, source, file_name=None, source_line=None, is_global=False, **kwargs):
        return self.root.interpreter.exec(source,
                                          file_name or self.file_name,
                                          source_line or self.source_line,
                                          is_global, **kwargs)

    def eval(self, source, file_name=None, source_line=None, is_global=False, **kwargs):
        return self.root.interpreter.eval(source,
                                          file_name or self.file_name,
                                          source_line or self.source_line,
                                          is_global, **kwargs)

    def raise_exception(self, klass, *args, extra_traceback=None, **kwargs):
        if extra_traceback is not None:
            raise klass(self.file_name, self.source_line, *args, **kwargs)
        else:
            raise klass(self.file_name, self.source_line, *args, **kwargs).with_traceback(extra_traceback)

    def abs_path(self, relative_path):
        if self.file_name == "<ujml_input>":
            return os.path.abspath(relative_path)
        elif os.path.isabs(relative_path):
            return relative_path
        else:
            return os.path.normpath(os.path.join(os.path.dirname(self.file_name), relative_path))

    @property
    def children(self):
        if self.__children is None:
            self.update_children()
        return self.__children

    def update_children(self):
        self.__children = []
        for element in self.element:
            self.create_child(element)

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def create_child(self, element: etree.ElementBase):
        """This function looks for the type of a child node."""
        # If this is a ref element. Find the element it references and add it as a child.
        if element.tag == "ref":
            node_id = element.get("id")
            child = self.find_node_by_id(node_id)
            if child is None:
                raise IdNotFoundError(self.file_name, element.sourceline, node_id)
        else:
            # Check if this is a data Data element
            if isinstance(inspect.getattr_static(self, element.tag, None), Data):
                from urban_journey.ujml.basic_nodes.data import data
                klass = data
            else:
                # Check if parent element knows what type it is.
                klass = self.child_lookup(element)

            # Update the node_register if it's empty.
            if len(node_register) == 0:
                update_extensions()

            # Look for node class in the register.
            if klass is None:
                if element.tag in node_register:
                    klass = node_register[element.tag]
                else:
                    # Node type was not found.
                    raise UnknownElementError(self.file_name, element.sourceline, element.tag)
            child = klass(element, self.root)

        # Add child
        self.add_child(child)

    def child_lookup(self, element: etree.ElementBase):
        """
        This function when overridden must return a class inheriting NodeBase or None. If None is returned then the child type will
        be searched in the node and module register.
        """
        pass
