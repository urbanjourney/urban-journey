import os
import inspect

from lxml import etree

from urban_journey.common.cached import cached
from urban_journey.ujml.plugin_register import node_register, update_plugins
from urban_journey.ujml.exceptions import UnknownElementError, IdNotFoundError, MissingSuperInitError
from urban_journey.ujml.attributes import String, Data


class NodeBase:
    """
    Base class for all nodes.

    :param element: Lxml element in the ujml document
    :type element: etree.ElementBase
    :param root: Root ujml element
    :type root: :class: `urban_journey.UjmlNode`
    """
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
        """
        Returns xml tag name

        :rtype: String
        """
        return self.element.tag

    def add_parent(self, parent):
        """
        Add a parent node to this node.

        :param parent: Parent NodeBase instance.
        :type parent: urban_journey.UjmlNode
        """
        if parent not in self.parents:
            self.parents.append(parent)
            parent.add_child(self)

    def add_child(self, child):
        """
        Add a child node to this node.

        :param child: Child NodeBase instance.
        :type child: urban_journey.NodeBase
        """
        if child not in self.children:
            self.children.append(child)
            child.add_parent(self)

    def remove_parent(self, parent):
        """
        Remove a parent element.

        :param parent: Parent NodeBase instance.
        :type parent: urban_journey.NodeBase
        """
        if parent in self.parents:
            self.parents.remove(parent)
            parent.remove_child(self)

    def remove_child(self, child):
        """
        Remove a child element.

        :param child: Child NodeBase instance.
        :type child: urban_journey.NodeBase"""
        if child in self.children:
            self.children.remove(child)
            child.remove_parent(self)

    def find_node_by_id(self, node_id):
        """
        Find a node by id anywhere in the document. Returns ``None`` if not found.

        :param id: Target node id
        :rtype: :class:`urban_journey.NodeBase` or ``None``

        .. note::
           Only looks for elements that have already been read. If target node has not been read yet, it won't be found.
           This will be fixed in the future.
        """
        if node_id in self.root.node_dict_by_id:
            return self.root.node_dict_by_id[node_id]

    @property
    def root(self):
        """
        The document root element

        :rtype: urban_journey.UjmlNode"""
        return self.__root

    @cached
    def file_name(self):
        """
        The document file name.

        :rtype: String
        """
        return self.root.file_name

    @cached
    def source_line(self):
        """
        The line number of this element inside the ujml file.

        :rtype: Integer
        """
        return self.element.sourceline

    def exec(self, source, file_name=None, source_line=None, is_global=False, **kwargs):
        """
        Execute python source in the embedded python interpreter.

        :param source: Python source to execute.
        :param file_name: File name to give to interpreter. Default is ujml document name.
        :param source_line: Source line of the first in the code snippet to be executed. Default is this elements source
           line.
        :param is_global: True to execute the code in the global scope.
        :param \*\*kwargs: Any other parameters passed, will the made available in the local scope. These parameters are
           ignored if ``isglobal`` is ``False``

        :type source: String
        :type file_name: String
        :type source_line: Integer
        :type is_global: Bool
        """
        return self.root.interpreter.exec(source,
                                          file_name or self.file_name,
                                          source_line or self.source_line,
                                          is_global, **kwargs)

    def eval(self, source, file_name=None, source_line=None, is_global=False, **kwargs):
        """
        Evaluate python source in the embedded python interpreter.

        :param source: Python source to execute.
        :param file_name: File name to give to interpreter. Default is ujml document name.
        :param source_line: Source line of the first in the code snippet to be executed. Default is this elements source
           line.
        :param is_global: True to execute the code in the global scope.
        :param \*\*kwargs: Any other parameters passed, will the made available in the local scope. These parameters are
           ignored if ``isglobal`` is ``False``

        :type source: String
        :type file_name: String
        :type source_line: Integer
        :type is_global: Bool

        :rtype: object
        """
        return self.root.interpreter.eval(source,
                                          file_name or self.file_name,
                                          source_line or self.source_line,
                                          is_global, **kwargs)

    def raise_exception(self, klass, *args, extra_traceback=None, **kwargs):
        """
        Used to raise a ujm exception.

        :param klass: Child class of BaseUJMLError.
        :param extra_traceback: Extra traceback information to be appended to the exception.
        :param \*args: Extra parameters that ``klass`` needs to initialize.
        :param \*\*kwargs: Extra parameters that ``klass`` needs to initialize.
        """
        if extra_traceback is not None:
            raise klass(self.file_name, self.source_line, *args, **kwargs)
        else:
            raise klass(self.file_name, self.source_line, *args, **kwargs).with_traceback(extra_traceback)

    def abs_path(self, relative_path):
        """
        Returns an absolute path for a file relative to the ujml file.

        :param relative_path: Path relative to ujml document.
        :rtype: String
        """
        if self.file_name == "<ujml_input>":
            return os.path.abspath(relative_path)
        elif os.path.isabs(relative_path):
            return relative_path
        else:
            return os.path.normpath(os.path.join(os.path.dirname(self.file_name), relative_path))

    @property
    def children(self):
        """
        List of children.

        :rtype: List of :class:`urban_journey.NodeBase`."""
        if self.__children is None:
            self.update_children()
        return self.__children

    def update_children(self):
        """Read all child elements from the ujml file."""
        if self.__children is None:
            self.__children = []
            for element in self.element:
                self.create_child(element)

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)

    def create_child(self, element: etree.ElementBase):
        """
        Finds NodeBase child class for a child element. There is no need to use this function. If this lookup
        behaviour has to be customized, override child_lookup(..) instead.
        """
        if element.tag is etree.Comment:
            return

        if element.tag is etree.PI:
            return

        # If this is a ref element. Find the element it references and add it as a child.
        if element.tag == "ref":
            node_id = element.get("id")
            child = self.find_node_by_id(node_id)
            if child is None:
                raise IdNotFoundError(self.file_name, element.sourceline, node_id)
        else:
            # Check if this is a data Data element
            if isinstance(inspect.getattr_static(self, element.tag, None), Data):
                from urban_journey.ujml.nodes.data import data
                klass = data
            else:
                # Check if parent element knows what type it is.
                klass = self.child_lookup(element)

            # Update the node_register if it's empty.
            if len(node_register) == 0:
                update_plugins()

            # Look for node class in the register.
            if klass is None:
                if element.tag in node_register:
                    klass = node_register[element.tag]
                else:
                    # Node type was not found.
                    raise UnknownElementError(self.file_name, element.sourceline, element.tag)
            child = klass(element, self.root)

        if not hasattr(child, "element"):
            self.raise_exception(MissingSuperInitError, self.tag, element.tag)

        # Add child
        self.add_child(child)

    def child_lookup(self, element: etree.ElementBase):
        """
        This function when overridden must return a class inheriting NodeBase or None. If None is returned then the child type will
        be searched in the node and module register.
        """
        pass

    def xpath(self, _path, namespaces=None, extensions=None, smart_strings=True, **_variables):
        return self.element.xpath(_path, namespaces, extensions, smart_strings, **_variables).node