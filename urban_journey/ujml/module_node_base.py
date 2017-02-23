from .node_base import NodeBase
from urban_journey.pubsub.module_base import ModuleBase


class ModuleNodeBase(NodeBase, ModuleBase):
    """
    Bases: :class:`urban_journey.NodeBase`, :class:`urban_journey.ModuleBase`

    Base class for all publisher, subscriber module nodes.

    :param element: Lxml element in the ujml document
    :type element: etree.ElementBase
    :param root: Root ujml element
    :type root: :class: `urban_journey.UjmlNode`
    """
    def __init__(self, element, root):
        NodeBase.__init__(self, element, root)
        ModuleBase.__init__(self, self.root.channel_register)
        self.__get_channel_names()

    def __get_channel_names(self):
        """Returns a dictionary containing the channel name that each port will connect to when subscribed."""
        for port_name in self.ports:
            channel_name = self.element.get(port_name)
            if channel_name is None:
                continue
            self.channel_names[port_name] = channel_name
