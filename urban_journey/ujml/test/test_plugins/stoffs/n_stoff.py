from urban_journey import ModuleNodeBase, activity, Clock


class n_stoff(ModuleNodeBase):
    clk1 = Clock()
    clk2 = Clock()
    clk3 = Clock()

    def __init__(self, e, r):
        super().__init__(e, r)
        self.clk1.period = 0.01
        self.clk1.start()
        self.clk2.period = 0.05
        self.clk2.start()
        self.clk3.period = 0.08
        self.clk3.start()

    @activity(clk1 & clk2 & clk3)
    async def tick(self):
        self.root.stop()
        self.clk1.stop()
        self.clk2.stop()
        self.clk3.stop()
