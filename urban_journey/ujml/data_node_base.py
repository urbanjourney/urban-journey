from abc import ABCMeta, abstractmethod

from lxml import etree

from urban_journey.ujml.node_base import NodeBase


class DataNodeBase(NodeBase, metaclass=ABCMeta):
    """
    Bases: :class:`urban_journey.NodeBase`

    Base class for all nodes that load in, generate or process input data.

    :param element: Lxml element in the ujml document
    :type element: etree.ElementBase
    :param root: Root ujml element
    :type root: :class: `urban_journey.UjmlNode`
    """
    def __init__(self, element: etree.ElementBase, root):
        super().__init__(element, root)
        self.root.data.add_data_node(self)

    @property
    @abstractmethod
    def data(self):
        """This abstract property should return the data enclosed in this data element."""
        pass

    def reset(self):
        """In cased the data is cached, this function should clear the cache to allow the data to be reloaded or
        recalculated."""
        pass
