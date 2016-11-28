from urban_journey import ModuleNodeBase, Input, activity


class m_stoff(ModuleNodeBase):
    inp = Input()

    def __init__(self, e, r):
        super().__init__(e, r)
        self.subscribe()

    @activity(inp)
    async def handle(self, inp):
        assert inp == "qwertyuiop"
        self.root.stop()
