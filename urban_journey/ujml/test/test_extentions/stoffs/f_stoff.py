"""
Pubsub module test modules.
"""

from urban_journey import ModuleNodeBase, activity, Output, Input, Eval


class f_stoff(ModuleNodeBase):
    """Producing test module."""
    op = Output(channel_name="foo")
    ip = Input(channel_name="foo")
    s = Eval()

    def __init__(self, element, root):
        super().__init__(element, root)
        self.subscribe()

    async def transmit(self):
        await self.op.flush("Some data")

    @activity(ip)
    async def op_handler(self, ip):
        assert ip == "Some data"
        s = self.eval('s')
        s.release()
