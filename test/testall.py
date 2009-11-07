import unittest
import sys
sys.path.append("/home/hattori/work/pyrg/")
import pyrg


class ColorFunctionTest(unittest.TestCase):

    def test_coloring_method(self):
        line = "get_gg (__main__.TestTest)"
        self.assertEqual("[36mget_gg (__main__.TestTest)[0m",
                         pyrg.coloring_method(line))

    def test_ngroute(self):
        input_strings = """..
        ----------------------------------------------------------------------
        Ran 2 tests in 0.000s

        OK
        """
        result_strings = """[32m.[0m[32m.[0m
        ----------------------------------------------------------------------
        Ran 2 tests in 0.000s

        OK
        """
        self.assertEqual(pyrg.parse_unittest_result(input_strings.splitlines()),
                         result_strings)


if __name__ == '__main__':
    unittest.main()
