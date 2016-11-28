from urban_journey import DataNodeBase, FilePath, NodeBase, ModuleNodeBase, Data, Input, Output, activity
from collections import OrderedDict

from urban_journey.exceptions import InvalidChildError


class field(DataNodeBase):
    file_path = FilePath(name="file")

    def __init__(self):
        with open(self.file_path) as f:
            pass

        self.r_e = 0
        self.mu = 0

    @property
    def data(self):
        return self


class GravityObjBase(ModuleNodeBase):
    def __init__(self, e, r):
        super().__init__(e, r)
        self.calculate_gravities = self.parents[0].calculate_gravities


class cb(GravityObjBase):
    field = Data()

    pos = Input()
    dcm = Input()

    f_g = Output()

    def __init__(self, e, r):
        super().__init__(e, r)
        self.channel_names['f_g'] = "f_g_" + self.id

    @activity(pos & dcm)
    async def handle(self, pos, dcm):
        await self.calculate_gravities(self, pos, self.field, dcm)


class sat(GravityObjBase):
    pos = Input()
    mass = Input()

    f_g = Output()

    def __init__(self, e, r):
        super().__init__(e, r)
        self.channel_names['f_g'] = "f_g_" + self.id

    @activity(pos & mass)
    async def handle(self, pos, mass):
        await self.calculate_gravities(self, pos, mass, dcm)


class Gravity(NodeBase):
    def __init__(self, e, r):
        super().__init__(e, r)
        self.objects = OrderedDict()
        self.n_objects_received = 0
        self.reset()

    def reset(self):
        self.n_objects_received = 0
        for child in self.children:
            self.objects[child] = None

    def child_lookup(self, element):
        if element.tag == "cb":
            return cb
        elif element.tag == "sat":
            return sat
        else:
            self.raise_exception(InvalidChildError, self.tag, element.tag)

    async def calculate_gravities(self, child, *args):
        self.objects[child] = args
        self.n_objects_received += 1

        if self.n_objects_received >= len(self.objects):
            pass
            for child_1, (pos_1, field_1, dcm_1) in self.objects:
                for child_2, (pos_2, field_2, dcm_2) in self.objects:
                    if child_1 is child_2:
                        continue

                    # Do Calculations here.

                await child_1.f_g(result)





