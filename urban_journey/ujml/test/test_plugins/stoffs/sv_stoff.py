from urban_journey import activity, Input, Output, ModuleNodeBase, Clock


class sv_stoff(ModuleNodeBase):
    clk1 = Clock()
    clk2 = Clock()
    out = Output(channel_name="foo")
    inp = Input(channel_name="foo")

    def __init__(self, e, r):
        super().__init__(e, r)
        self.subscribe()
        self.clk1.period = 0.02
        self.clk2.period = 0.05
        self.clk1.start()
        self.clk2.start()
        self.i = 0

        self.inp_trigger_count = 0

    @activity(clk1)
    async def clk1_tick(self):
        self.i += 1
        await self.out.flush(self.i)

    @activity(inp | clk2)
    async def asdfg(self, inp):
        if inp is not None:
            self.inp_trigger_count += 1
        else:
            assert self.i == 2
            assert self.inp_trigger_count == 2
            self.clk1.stop()
            self.clk2.stop()
            self.root.stop()
