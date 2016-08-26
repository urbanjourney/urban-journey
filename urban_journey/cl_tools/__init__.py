from collections import OrderedDict

from .run import run

from .list import list
from .init import init
from .test_command import test
from .update import update

cl_tools = OrderedDict([
    ("init", init),
    ("run", run),
    ("list", list),
    ("test", test),
    ("update", update)
])
