import os

from lxml import etree

from urban_journey.common.cached import cached
from urban_journey.ujml.register import node_register, update_node_register
from urban_journey.ujml.exceptions import UnknownElementError


class NodeBase:
    def __init__(self, element: etree.ElementBase, root):
        element.node = self
        self.element = element
        self.parents = []
        self.__children = None
        self.__file_name = None
        self.__root = root

    @cached
    def tag(self):
        return self.element.tag

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child):
        child.add_parent(self)
        self.children.append(child)

    @property
    def root(self):
        return self.__root

    @cached
    def file_name(self):
        return self.root.file_name

    @cached
    def source_line(self):
        return self.element.sourceline

    def exec(self, source, file_name, source_line, is_global=False, **kwargs):
        return self.root.interpreter.exec(source, file_name, source_line, is_global, **kwargs)

    def eval(self, source, file_name, source_line, is_global=False, **kwargs):
        return self.root.interpreter.eval(source, file_name, source_line, is_global, **kwargs)

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
            return os.path.join(os.path.dirname(self.file_name), relative_path)

    @property
    def children(self):
        if self.__children is None:
            self.update_children()
        return self.__children

    def update_children(self):
        self.__children = []
        for element in self.element:
            self.__create_child(element)

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def __create_child(self, element: etree.ElementBase):
        """This function looks for the type of a child node."""
        klass = self.child_lookup(element)
        if len(node_register) == 0:
            update_node_register()

        if klass is None and element.tag in node_register:
            klass = node_register[element.tag]
        else:
            # Node type was not found. For now, raise exception
            raise UnknownElementError(self.file_name, element.sourceline, element.tag)
        child = klass(element, self.root)
        self.add_child(child)

    def child_lookup(self, element: etree.ElementBase):
        """
        This function must return a class inheriting NodeBase or None. If None is returned then the child type will
        be searched in the node and module register.
        """
        pass
