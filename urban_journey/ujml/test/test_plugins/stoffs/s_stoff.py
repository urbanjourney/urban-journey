from urban_journey import ModuleNodeBase, Clock, activity, String


class s_stoff(ModuleNodeBase):
    """
    Module node that raises an exception.
    """
    clk = Clock()

    error_type = String(optional_value="exception")

    def __init__(self, e, r):
        super().__init__(e, r)

        self.clk.period = 1
        self.clk.start()

    @activity(clk)
    async def tick(self):
        if self.error_type == "assert":
            assert 1 == 2
        else:
            raise Exception("s_stoff: Exception")
