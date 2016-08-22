import unittest
from threading import Semaphore
import asyncio

from urban_journey import from_string, extension_paths, update_extensions, __version__ as uj_version, get_event_loop
from .test_extentions import __path__ as test_ext_path


class TestPubSubNodes(unittest.TestCase):
    def setUp(self):
        # Add the test extensions.
        if test_ext_path[0] not in extension_paths:
            extension_paths.append(test_ext_path[0])
            update_extensions()

    def test_simple_input_output_ports(self):
        ujml_code = '<?xml version="1.0"?><ujml version="{}">'.format(uj_version) + '''
                       <f_stoff/>
                    </ujml>'''
        s = Semaphore(0)
        globs = {"s": s}
        ujml = from_string(ujml_code, globals=globs)
        print(ujml)
        loop = get_event_loop()
        asyncio.run_coroutine_threadsafe(ujml[0].transmit(), loop=loop)
        assert s.acquire(timeout=0.1)


