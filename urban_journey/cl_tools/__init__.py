from collections import OrderedDict

from .run import run

from .list import list
from .init import init
from .command_test import test
from .update import update
from .clear import clear


# An Ordered dictionary with all the available command line commands.
cl_tools = OrderedDict([
    ("init", init),
    ("run", run),
    ("list", list),
    ("test", test),
    ("update", update),
    ("clear", clear)
])
