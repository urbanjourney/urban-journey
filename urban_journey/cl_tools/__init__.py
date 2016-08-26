from collections import OrderedDict

from .run import run

from .extensions import ext
from .init import init
from .test_command import test
from .update import update

cl_tools = OrderedDict([
    ("init", init),
    ("run", run),
    ("ext", ext),
    ("test", test),
    ("update", update)
])
