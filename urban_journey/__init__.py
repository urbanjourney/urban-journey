# Urban journey API

__version__ = "0.0.1"

import sys

if sys.platform == "win32":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)


# Publisher subscriber framework
from urban_journey.pubsub.activity import activity, ActivityBase, ActivityMode
from urban_journey.pubsub.ports.input import InputPortStatic as Input, InputPort
from urban_journey.pubsub.ports.output import Output, OutputPort
from urban_journey.pubsub.trigger import TriggerBase
from urban_journey.pubsub.module_base import ModuleBase
from urban_journey.pubsub.channels.channel_register import ChannelRegister
from urban_journey.pubsub.trigger.condition_and import ConditionAnd


# Urban Journey Markup Language (UJML)
from urban_journey.ujml.node_base import NodeBase
from urban_journey.ujml.data_node_base import DataNodeBase
from urban_journey.ujml.module_node_base import ModuleNodeBase
from urban_journey.ujml.root_ujml_node import UjmlNode
from urban_journey.ujml.unique import Empty, Required
from urban_journey.ujml.attributes import *
from urban_journey.ujml.loaders import from_string, from_file
from urban_journey.ujml.plugin_register import plugin_paths, node_register, update_plugins
from urban_journey.ujml.widget_node_base import QWidgetNodeBase, UjQtSignal
from urban_journey.ujml.interpreter import UJMLPythonInterpreter
from urban_journey.ujml.data_container import DataContainer


# General stuff
from urban_journey.event_loop import get as get_event_loop, get_thread as get_event_thread
from urban_journey.uj_project import UjProject
# from urban_journey.clock import clock_descriptor_factory as Clock

from urban_journey.new_clock import ClockStatic as Clock
