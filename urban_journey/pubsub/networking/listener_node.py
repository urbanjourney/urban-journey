from urban_journey.pubsub.networking.listener import Listener
from urban_journey.pubsub.networking.connection import Connection

from urban_journey.ujml.module_node_base import ModuleNodeBase
from urban_journey.ujml.attributes.std_types import String, Int

from urban_journey.exceptions import UjValueError


class ListenerNode(ModuleNodeBase):
    """
    This nodes creates a opens a port and starts listening for incoming connections.
    """

    host = String()
    port = Int()

    def __init__(self, e, r):
        super().__init__(e, r)

        # Check if port number is valid
        if self.port <= 0 or self.port >= 65535:
            self.raise_exception(UjValueError, "The port number must be between 0 and 65535")

        # Open listener.
        self.listener = Listener(self.host, self.port, self.root.connections)
