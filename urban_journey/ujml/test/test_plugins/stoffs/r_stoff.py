from urban_journey import Input, Output, activity, Clock, ModuleNodeBase


class r_stoff(ModuleNodeBase):
    """
    Module node that uses a ConditionAnd to trigger one of it's activities.
    """

    clk1 = Clock()
    clk2 = Clock()
    out = Output(channel_name="foo")
    inp = Input(channel_name="foo")

    def __init__(self, e, r):
        super().__init__(e, r)
        self.subscribe()
        self.clk1.start()
        self.clk1.period = 0.02
        self.clk2.period = 0.05
        self.clk2.start()
        self.i = 0

    @activity(clk1)
    async def clk1_tick(self):
        self.i += 1
        await self.out.flush(self.i)

    @activity(inp & clk2)
    async def asdfg(self, inp):
        assert inp == 2
        self.clk1.stop()
        self.clk2.stop()
        self.root.stop()
