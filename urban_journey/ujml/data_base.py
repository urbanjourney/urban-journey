from abc import ABCMeta, abstractmethod

from urban_journey.ujml.node_base import NodeBase


class DataNodeBase(NodeBase, metaclass=ABCMeta):
    @property
    @abstractmethod
    def data(self):
        """This property should return the data enclosed in this data element."""
        pass

    def reset(self):
        """In cased the data is cached, this function should clear the cache to allow the data to be reloaded or
        recalculated."""
        pass
