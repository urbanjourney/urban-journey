"""
Pubsub module test modules.
"""

from urban_journey import ModuleNodeBase, activity, Output, Input


class f_stoff(ModuleNodeBase):
    """Producing test module."""
    op = Output(channel_name="foo")
    ip = Input(channel_name="foo")

    async def transmit(self):
        await self.op.flush("Some data")

    @activity(ip)
    async def op_handler(self, ip):
        print(ip)
        s = self.eval('s')
        print(s)
        s.release()
