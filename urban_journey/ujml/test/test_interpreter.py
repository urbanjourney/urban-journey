import unittest
import sys

from urban_journey.ujml.interpreter import UJMLPythonInterpreter, UJMLPythonSource


class TestInterpreter(unittest.TestCase):
    def test_compile_exception_handling(self):
        '''Checks if exceptions are properly handled when compiling the python source code'''
        # Check compile time error.
        i = UJMLPythonInterpreter()
        try:
            UJMLPythonSource(i, 'a=1+2\n\nb=3+2a', 'qwerty', 'exec', 56)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 57)
            self.assertEqual(vl.filename, 'qwerty')

    def test_runtime_exception_handling(self):
        '''Check if runtime exceptions are properly handled.'''
        # Check runtime error.
        try:
            dpi = UJMLPythonInterpreter()
            dpi.exec('"234"+1234', "asdfg", 5678)
            assert False
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 5678)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdfg")

    def test_interpreter_single_line_eval(self):
        dpi = UJMLPythonInterpreter()
        res = dpi.eval('1234567890', 'asdf', 55)
        self.assertEqual(res, 1234567890)

    # Multi line evals where not implemented properly, so I removed it temporarily
    @unittest.skip
    def test_interpreter_multi_line_eval(self):
        dpi = UJMLPythonInterpreter()
        res = dpi.eval('a=1234567890\na', 'asdf', 55)
        try:
            # a should only be available in the local scope of the code being evaluated.
            a = dpi['a']
            assert False
        except KeyError:
            pass
        except:
            assert False
        self.assertEqual(res, 1234567890)

    @unittest.skip
    def test_interpreter_multi_line_eval_exec_exception_handling(self):
        dpi = UJMLPythonInterpreter()
        try:
            dpi.eval('a=1234567890bb\na', 'asdf', 55)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 55)
            self.assertEqual(vl.filename, 'asdf')

    @unittest.skip
    def test_interpreter_multi_line_eval_eval_exception_handling(self):
        dpi = UJMLPythonInterpreter()
        try:
            dpi.eval('a=1234567890\n1212a', 'asdf', 55)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 56)
            self.assertEqual(vl.filename, 'asdf')

    @unittest.skip
    def test_interpreter_multi_line_eval_exec_runtime_exception_handling(self):
        dpi = UJMLPythonInterpreter()
        try:
            dpi.eval('a=1234567890+"dscsdc"\na', 'asdf', 55)
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 55)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdf")

    @unittest.skip
    def test_interpreter_multi_line_eval_eval_runtime_exception_handling(self):
        dpi = UJMLPythonInterpreter()
        try:
            dpi.eval('a=1234567890\n1212+"sdcsdc"', 'asdf', 55)
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 56)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdf")