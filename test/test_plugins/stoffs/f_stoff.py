"""
Pubsub module test modules.
"""

from urban_journey import ModuleNodeBase, activity, Output, Input


class f_stoff(ModuleNodeBase):
    # Create ports
    op = Output(channel_name="foo")
    ip = Input(channel_name="foo")

    # Subscribe to channels in constructor
    def __init__(self, element, root):
        super().__init__(element, root)
        self.subscribe()

    # This coroutine is called from elsewhere.
    async def transmit(self):
        # Send data through the output port by just calling the port and passing the data as a parameter.
        # This is a coroutine so remember to await when sending (like in this case) or later before the
        # function returns.
        await self.op("Some data")

    @activity(ip)
    async def op_handler(self, ip):
        # The data that was transmitted will be passed as a parameter.
        assert ip == "Some data"
        s = self.eval('s')
        s.release()
