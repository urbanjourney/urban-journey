from urban_journey import activity, InputPort, OutputPort, ModuleNodeBase


class t_stoff(ModuleNodeBase):
    def __init__(self, e, r):
        super().__init__(e, r)

        self.inp = InputPort(self, "data", "foo")
        self.out = OutputPort(self.channel_register, "data", "foo")

        self.inp.subscribe()
        self.out.subscribe()

        self.out.flush_threadsafe("Here's Johnny!")

        self.handler.trigger_obj = self.inp

    @activity(None)
    async def handler(self, data):
        assert data == "Here's Johnny!"
        self.root.stop()
