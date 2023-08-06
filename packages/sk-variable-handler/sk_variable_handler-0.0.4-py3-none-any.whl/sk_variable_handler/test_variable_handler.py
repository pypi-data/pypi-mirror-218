from .variable_handler import VariableHandler
from sk_calculator import Calculator
import unittest


class TestGetValues(unittest.TestCase):
    def setUp(self):
        self.variable = VariableHandler()
        self.calculator = Calculator()
        self.variable.set_calculator(self.calculator)

    def test_get_result(self):
        declarations = "$x=1+2;$y=2+1;$var=12+223+(222+2)+sin(90);$var2=$x+$y;$xy=($var2+$x+$y);$yx=$xy+$var2"
        expected_result = {'$x': 3, '$y': 3, '$var': 460, '$var2': 6, '$xy': 12, '$yx': 18}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_empty_declaration(self):
        # Test when there are no variable declarations
        declarations = ""
        expected_result = {}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_single_declaration(self):
        # Test when there is only one variable declaration
        declarations = "$x=10"
        expected_result = {'$x': 10}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_multiple_declarations(self):
        # Test when there are multiple variable declarations
        declarations = "$x=1;$y=2;$z=3"
        expected_result = {'$x': 1, '$y': 2, '$z': 3}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_duplicate_declarations(self):
        # Test when there are duplicate variable declarations
        declarations = "$x=1;$y=2;$x=3"
        expected_result = {'$x': 3, '$y': 2}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_invalid_declaration(self):
        # Test when there is an invalid variable declaration
        declarations = "$x=1+"
        expected_result = {'$x': ['Syntax Error: Incomplete expression at 1+']}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_with_spaces(self):
        # Test when there are spaces in the variable declarations
        declarations = "$x = 1 + 2 ; $y = 2 + 1 ; $var = 12 + 223 + (222 + 2) + sin(90) ; $var2 = $x + $y ; $xy = ($var2 + $x + $y) ; $yx = $xy + $var2"
        expected_result = {'$x': 3, '$y': 3, '$var': 460, '$var2': 6, '$xy': 12, '$yx': 18}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_case_sensitive(self):
        # Test when variable names are case sensitive
        declarations = "$X = 1 ; $x = 2 ; $X = $x + 3"
        expected_result = {'$X': 5, '$x': 2}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_with_trailing_semicolon(self):
        # Test when there is a trailing semicolon in the declarations
        declarations = "$x = 1 + 2 ;"
        expected_result = {'$x': 3}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_with_newlines(self):
        # Test when there are newlines in the variable declarations
        declarations = "$x = 1 + 2 ;\n$y = 2 + 1 ;\n$z = $x + $y"
        expected_result = {'$x': 3, '$y': 3, '$z': 6}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_get_result_with_comments(self):
        # Test when there are comments in the variable declarations
        declarations = "$x = 1 + 2 ; # Variable x\n$y = 2 + 1 ; # Variable y\n$z = $x + $y"
        expected_result = {'$x': 3, '$y': 3, '$z': 6}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_nested_variable(self):
        # Test when there are comments in the variable declarations
        declarations = "$x = 1;$x = $x+1;$y = [$x];$z = [$x,$y];$xy = [$x,$y,$z];"
        expected_result = {'$x': 2, '$xy': [2, [2], [2, [2]]], '$y': [2], '$z': [2, [2]]}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_recursive_variable(self):
        declarations = "$x = 1 ;$x = $x+1;$x = $x+1;$x = $x+1;$x = $x+1;"
        expected_result = {'$x': 5}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_recursive_variable2(self):
        declarations = "$x = 1 ;$x = $x+1;$x = $x+1;$x = $x+1;$x = $x+1;"
        expected_result = {'$x': 5}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

    def test_recursive_variable3(self):
        declarations = "$x = 'hi';$y = 'there';$z = $x+' '+ $y;"
        expected_result = {'$x': 'hi', '$y': 'there', '$z': 'hi there'}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)

        declarations = "$x = 'hi there';$y = $x + ' ' + 'how are you';$a = 1;$b = $a+1;$list = [$x,$y,$a,$b];"
        expected_result = {'$x': 'hi there', '$y': 'hi there how are you', '$a': 1, '$b': 2,
                           '$list': ['hi there', 'hi there how are you', 1, 2]}
        result = self.variable.get_result(declarations)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
