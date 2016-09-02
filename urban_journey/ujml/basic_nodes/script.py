from urban_journey import NodeBase
from urban_journey import FilePath, Bool, get_event_loop

from lxml import etree


class script(NodeBase):
    src = FilePath(optional_value=None)
    async = Bool(optional_value=False)

    def __init__(self, element: etree.ElementBase, root):
        super().__init__(element, root)
        if self.src is None:
            source = self.element.text
        else:
            with open(self.src) as f:
                source = f.read()

        if self.async:
            # Not sure how this would be useful because of the GIL, but whatever. This loop runs on a separate thread.
            loop = get_event_loop()
            loop.call_soon(self.exec, source)
        else:
            self.exec(source, is_global=True)
