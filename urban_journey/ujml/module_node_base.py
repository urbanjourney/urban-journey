from .node_base import NodeBase
from urban_journey.pubsub.module_base import ModuleBase


class ModuleNodeBase(NodeBase, ModuleBase):
    def __init__(self, element, root):
        NodeBase.__init__(self, element, root)
        ModuleBase.__init__(self, self.root.channel_register)
