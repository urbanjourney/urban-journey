import unittest
from threading import Semaphore
import asyncio

from urban_journey import from_string, plugin_paths, update_plugins, __version__ as uj_version, get_event_loop
from .test_plugins import __path__ as test_ext_path


class TestPubSubNodes(unittest.TestCase):
    def setUp(self):
        # Add the test plugins.
        if test_ext_path[0] not in plugin_paths:
            plugin_paths.append(test_ext_path[0])
            update_plugins()

    def test_simple_input_output_ports(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                       <f_stoff s="s"/>
                    </ujml>'''
        s = Semaphore(0)
        globs = {"s": s}
        ujml = from_string(ujml_code, globals=globs)
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(ujml[0].transmit(), loop=loop)
        assert s.acquire(timeout=0.1)

    def test_alternate_channel_name(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                       <f_stoff s="s" op="bar" ip="bar"/>
                    </ujml>'''
        s = Semaphore(0)
        globs = {"s": s}
        ujml = from_string(ujml_code, globals=globs)
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(ujml[0].transmit(), loop=loop)
        assert s.acquire(timeout=0.1)
        assert ujml[0].op.channel.name == "bar"
        assert ujml[0].ip.channel.name == "bar"

    def test_widget_node(self):
        # Warning: This test may potentially lock forever if failing. To fix this timeout param has to be implemented
        #          for 'UjmlNode.pyqt_start()'

        # Warning: This warning applies to all tests running coroutines. So all tests in the pubsub section.
        #
        #          It's for now impossible to handle exceptions occurring inside the event loop. So it is possible for a
        #          test to pass while an exception has occurred.
        #
        #          Most tests will timeout in case an exception occurs, but some test won't timeout or won't give a
        #          timeout warning (e.g. those doing stuff with PyQt like this one).

        ujml_code = '''<?xml version="1.0"?>
        <ujml pyqt="true" version="{uj_version}">
            <k_stoff out="foo"/>
            <m_stoff inp="foo"/>
        </ujml>
        '''.format(uj_version=uj_version)
        ujml = from_string(ujml_code)
        assert ujml.start(timeout=0.1)

    def test_condition_and(self):
        ujml_code = '''<?xml version="1.0"?>
                <ujml version="{uj_version}">
                    <n_stoff/>
                </ujml>
                '''.format(uj_version=uj_version)
        ujml = from_string(ujml_code)
        assert ujml.start(timeout=0.1)

    def test_condition_and_with_parameters(self):
        ujml_code = '''<?xml version="1.0"?>
                <ujml version="{uj_version}">
                    <r_stoff/>
                </ujml>
                '''.format(uj_version=uj_version)
        ujml = from_string(ujml_code)
        assert ujml.start(timeout=0.1)

    def test_ujml_node_exception_handler(self):
        ujml_code = '''<?xml version="1.0"?>
                        <ujml version="{uj_version}"
                              stop_on_exception="true">
                            <s_stoff error_type="assert"/>
                        </ujml>
                        '''.format(uj_version=uj_version)
        ujml = from_string(ujml_code)
        assert ujml.start(timeout=10)
