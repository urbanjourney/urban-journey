"""
Pubsub module test modules.
"""

from urban_journey import ModuleNodeBase, activity, Output, Input, Eval, String, Exec


class f_stoff(ModuleNodeBase):
    op = Output(channel_name="foo")
    ip = Input(channel_name="foo")

    def __init__(self, element, root):
        super().__init__(element, root)
        self.subscribe()

    async def transmit(self):
        self.op.data[0] = "Some data"
        await self.op.flush()

    @activity(ip)
    async def op_handler(self, ip):
        assert ip[0] == "Some data"
        s = self.eval('s')
        s.release()
