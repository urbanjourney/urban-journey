import unittest
import sys


class TestUJMLPythonInterpreter(unittest.TestCase):
    def test_compile_exception_handling(self):
        '''Checks if exceptions are properly handled when compiling the python source code'''
        from urban_journey.ujml.python_interpreter import UJMLPythonSourceClass

        # Check compile time error.
        try:
            UJMLPythonSourceClass('a=1+2\n\nb=3+2a', 'qwerty', 'exec', 55)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 57)
            self.assertEqual(vl.filename, 'qwerty')

    def test_runtime_exception_handling(self):
        '''Check if runtime exceptions are properly handled.'''
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass

        # Check runtime error.
        try:
            dpi = UJMLPythonInterpreterClass()
            dpi.exec('"234"+1234', "asdfg", 5678)
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 5678)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdfg")

    def test_interpreter_single_line_eval(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        res = dpi.eval('1234567890', 'asdf', 55)
        self.assertEqual(res, 1234567890)

    def test_interpreter_multi_line_eval(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        res = dpi.eval('a=1234567890\na', 'asdf', 55)
        self.assertEqual(res, 1234567890)

    def test_interpreter_multi_line_eval_exec_exception_handling(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        try:
            dpi.eval('a=1234567890bb\na', 'asdf', 55)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 55)
            self.assertEqual(vl.filename, 'asdf')

    def test_interpreter_multi_line_eval_eval_exception_handling(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        try:
            dpi.eval('a=1234567890\n1212a', 'asdf', 55)
        except SyntaxError:
            _, vl, _ = sys.exc_info()
            self.assertEqual(vl.lineno, 56)
            self.assertEqual(vl.filename, 'asdf')

    def test_interpreter_multi_line_eval_exec_runtime_exception_handling(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        try:
            dpi.eval('a=1234567890+"dscsdc"\na', 'asdf', 55)
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 55)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdf")

    def test_interpreter_multi_line_eval_eval_runtime_exception_handling(self):
        from urban_journey.ujml.python_interpreter import UJMLPythonInterpreterClass
        dpi = UJMLPythonInterpreterClass()
        try:
            dpi.eval('a=1234567890\n1212+"sdcsdc"', 'asdf', 55)
        except:
            _, _, tb = sys.exc_info()
            self.assertEqual(tb.tb_next.tb_next.tb_lineno, 56)
            self.assertEqual(tb.tb_next.tb_next.tb_frame.f_code.co_filename, "asdf")


if __name__ == '__main__':
    unittest.main()
