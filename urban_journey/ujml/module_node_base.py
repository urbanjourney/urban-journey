from .node_base import NodeBase
from urban_journey.pubsub.module_base import ModuleBase


class ModuleNodeBase(NodeBase, ModuleBase):
    def __init__(self, element, root):
        NodeBase.__init__(self, element, root)
        ModuleBase.__init__(self, self.root.channel_register)
        self.get_channel_names()

    def get_channel_names(self):
        for port_name in self.ports:
            channel_name = self.element.get(port_name)
            if channel_name is None:
                continue
            self.channel_names[port_name] = channel_name


