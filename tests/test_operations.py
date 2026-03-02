import pytest

from decimal import Decimal

from app.exceptions import ValidationError
from app.operations import AbsoluteDifference
from app.operations import Addition
from app.operations import Division
from app.operations import IntegerDivision
from app.operations import Modulus
from app.operations import Multiplication
from app.operations import Operation
from app.operations import OperationFactory
from app.operations import PercentageCalculation
from app.operations import Power
from app.operations import Root
from app.operations import Subtraction

class TestOperation:

    '''
    Test the base Operation class.
    '''

    def test_str_representation(self):

        # Test that str returns the class name.

        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a
            def validate_operands(self, a: Decimal, b: Decimal) -> None:
                pass

        assert str(TestOp()) == 'TestOp'

class BaseOperationTest:

    '''
    Use this class to facilitate paramterized testing, instead of the lengthy pytest.mark.parametrize.
    This also means testing will be standardized across different sub-classes.
    '''

    def test_valid_operations(self):

        # Test operation with valid inputs

        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected = Decimal(str(case['expected']))
            result = operation.execute(a, b)
            assert result == expected, f'Failed case: {name}'

    def test_invalid_operations(self):

        # Test operation with invalid inputs, and verify the correct errors were raised.

        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected_error = case['error']
            expected_message = case['message']
            with pytest.raises(expected_error, match=expected_message):
                operation.execute(a, b)

class TestAddition(BaseOperationTest):

    '''
    Test Addition operation
    '''

    operation_class = Addition
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '8'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '-8'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-2'},
        'zero_sum': {'a': '5', 'b': '-5', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '8.8'},
        'large_numbers': {'a': '1e10', 'b': '1e10', 'expected': '20000000000'},
    }
    invalid_test_cases = {}

class TestSubtraction(BaseOperationTest):

    '''
    Test Subtraction operation
    '''

    operation_class = Subtraction
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '2'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '-2'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-8'},
        'zero_result': {'a': '5', 'b': '5', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '2.2'},
        'large_numbers': {'a': '1e10', 'b': '1e9', 'expected': '9000000000'},
    }
    invalid_test_cases = {}

class TestMultiplication(BaseOperationTest):

    '''
    Test Multiplication operation
    '''

    operation_class = Multiplication
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '15'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '15'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-15'},
        'multiply_by_zero': {'a': '5', 'b': '0', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '18.15'},
        'large_numbers': {'a': '1e5', 'b': '1e5', 'expected': '10000000000'},
    }
    invalid_test_cases = {}

class TestDivision(BaseOperationTest):

    '''
    Test Division operation
    '''

    operation_class = Division
    valid_test_cases = {
        'positive_numbers': {'a': '6', 'b': '2', 'expected': '3'},
        'negative_numbers': {'a': '-6', 'b': '-2', 'expected': '3'},
        'mixed_signs': {'a': '-6', 'b': '2', 'expected': '-3'},
        'decimals': {'a': '5.5', 'b': '2', 'expected': '2.75'},
        'divide_zero': {'a': '0', 'b': '5', 'expected': '0'},
    }
    invalid_test_cases = {
        'divide_by_zero': {'a': '5', 'b': '0', 'error': ValidationError, 'message': 'Division by zero is not allowed'},
    }

class TestPower(BaseOperationTest):

    '''
    Test Power operation
    '''

    operation_class = Power
    valid_test_cases = {
        'positive_base_and_exponent': {'a': '2', 'b': '3', 'expected': '8'},
        'zero_exponent': {'a': '5', 'b': '0', 'expected': '1'},
        'one_exponent': {'a': '5', 'b': '1', 'expected': '5'},
        'decimal_base': {'a': '2.5', 'b': '2', 'expected': '6.25'},
        'zero_base': {'a': '0', 'b': '5', 'expected': '0'},
    }
    invalid_test_cases = {
        'negative_exponent': {'a': '2', 'b': '-3', 'error': ValidationError, 'message': 'Negative exponents not supported'},
    }

class TestRoot(BaseOperationTest):

    '''
    Test Root operation
    '''

    operation_class = Root
    valid_test_cases = {
        'square_root': {'a': '9', 'b': '2', 'expected': '3'},
        'cube_root':  {'a': '27', 'b': '3', 'expected': '3'},
        'fourth_root':  {'a': '16', 'b': '4', 'expected': '2'},
        'decimal_root': {'a': '2.25', 'b': '2', 'expected': '1.5'},
    }
    invalid_test_cases = {
        'negative_base': {'a': '-9', 'b': '2', 'error': ValidationError, 'message': 'Cannot calculate root of negative number'},
        'zero_root': {'a': '9', 'b': '0', 'error': ValidationError, 'message': 'Zero root is undefined'},
    }

class TestModulus(BaseOperationTest):

    '''
    Test Modulus operation
    '''

    operation_class = Modulus
    valid_test_cases = {
        'positive_integers': {'a': '8', 'b': '3', 'expected': '2'},
        'negative_integers': {'a': '-8', 'b': '-3', 'expected': '-2'},
        'positive_integer_and_negative_integer': {'a': '8', 'b': '-3', 'expected': '2'}, # Decimal result is 2, vs. -1 for int/float
        'negative_integer_and_positive_integer': {'a': '-8', 'b': '3', 'expected': '-2'}, # Decimal result is -2, vs 1 for int/float
        'positive_floats': {'a': '4.5', 'b': '2.5', 'expected': '2'},
        'negative_floats': {'a': '-4.5', 'b': '-2', 'expected': '-0.5'},
        'mixed_numbers': {'a': '4.5', 'b': '2', 'expected': '0.5'},
        'large_numbers': {'a': '1e10', 'b': '1e9', 'expected': '0'},
    }
    invalid_test_cases = {}

class TestIntegerDivision(BaseOperationTest):

    '''
    Test IntegerDivision operation
    '''

    operation_class = IntegerDivision
    valid_test_cases = {
        'positive_integers': {'a': '8', 'b': '3', 'expected': '2'},
        'negative_integers': {'a': '-8', 'b': '-3', 'expected': '2'},
        'positive_integer_and_negative_integer': {'a': '8', 'b': '-3', 'expected': '-2'}, # Decimal result is -2, vs. -3 for int/float
        'negative_integer_and_positive_integer': {'a': '-8', 'b': '3', 'expected': '-2'}, # Decimal result is -3, vs. -3 for int/float
        'positive_floats': {'a': '4.5', 'b': '2.5', 'expected': '1'},
        'negative_floats': {'a': '-4.5', 'b': '-2', 'expected': '2'},
        'mixed_numbers': {'a': '4.5', 'b': '2', 'expected': '2'},
        'large_numbers': {'a': '1e10', 'b': '1e9', 'expected': '10'},
    }
    invalid_test_cases = {}

class TestPercentageCalculation(BaseOperationTest):

    '''
    Test PercentCalculation operation
    '''

    operation_class = PercentageCalculation
    valid_test_cases = {
        'positive_integers': {'a': '10', 'b': '50', 'expected': '20'},
        'positive_floats': {'a': '4.5', 'b': '10', 'expected': '45'},
        'mixed_numbers': {'a': '0.005', 'b': '2.5', 'expected': '0.2'},
        'large_numbers': {'a': '1e9', 'b': '1e10', 'expected': '10'},
    }
    invalid_test_cases = {
        'negative_integer_and_positive_integer': {'a': '-5', 'b': '100', 'error': ValidationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'positive_integer_and_negative_integer': {'a': '5', 'b': '-100', 'error': ValidationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'negative_integers': {'a': '-5', 'b': '-100', 'error': ValidationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'negative_floats': {'a': '-5.5', 'b': '-1.5', 'error': ValidationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'zero_denominator': {'a': '-5.5', 'b': '0', 'error': ValidationError, 'message': 'Cannot calculate percentages when b \\(denominator\\) is 0'},
    }

class TestAbsoluteDifference(BaseOperationTest):

    '''
    Test AbsoluteDifference operation
    '''

    operation_class = AbsoluteDifference
    valid_test_cases = {
        'positive_integer_greater_than_positive_integer': {'a': '8', 'b': '3', 'expected': '5'},
        'positive_integer_less_than_positive_integer': {'a': '8', 'b': '10', 'expected': '2'},
        'negative_integer_greater_than_negative_integer': {'a': '-8', 'b': '-10', 'expected': '2'},
        'negative_integer_less_than_negative_integer': {'a': '-8', 'b': '-5', 'expected': '3'},
        'positive_integer_and_negative_integer': {'a': '8', 'b': '-9', 'expected': '17'},
        'negative_integer_and_positive_integer': {'a': '-8', 'b': '7', 'expected': '15'},
        'positive_float_greater_than_positive_float': {'a': '4.5', 'b': '2.4', 'expected': '2.1'},
        'positive_float_less_than_positive_float': {'a': '5.5', 'b': '6.7', 'expected': '1.2'},
        'negative_float_and_positive_float': {'a': '-2.1', 'b': '2.4', 'expected': '4.5'},
        'negative_float_greater_than_negative_float': {'a': '-2', 'b': '-4.5', 'expected': '2.5'},
        'negative_float_less_than_negative_float': {'a': '-4.5', 'b': '-3.5', 'expected': '1'},
        'mixed_numbers': {'a': '-4.5', 'b': '20', 'expected': '24.5'},
        'large_numbers': {'a': '1e9', 'b': '1e10', 'expected': '9e9'},
    }
    invalid_test_cases = {}

class TestOperationFactory:

    '''
    Test OperationFactory functionality
    '''

    def test_create_valid_operations(self):

        # Test creation of all valid operations

        operation_map = {
            'add': Addition,
            'subtract': Subtraction,
            'multiply': Multiplication,
            'divide': Division,
            'power': Power,
            'root': Root,
            'modulus': Modulus,
            'int_divide': IntegerDivision,
            'percent': PercentageCalculation,
            'abs_diff': AbsoluteDifference,
        }

        for op_name, op_class in operation_map.items():

            # Correct case
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)

            # Case insensitive
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):

        # Test creation of invalid operation

        with pytest.raises(ValueError, match='Unknown operation: invalid_op'):
            OperationFactory.create_operation('invalid_opp')

    def test_register_valid_operation(self):

        # Test registering a new valid operation

        class SomeOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a
            def validate_operands(self, a, b):
                pass

        OperationFactory.register_operation('new_op', SomeOperation)
        operation = OperationFactory.create_operation('new_op')
        assert isinstance(operation, SomeOperation)

    def test_register_invalid_operation(self):

        # Test registering an invalid operation, verify an error is raised

        class BadOperation:
            pass

        with pytest.raises(TypeError, match='Operation class must inherit'):
            OperationFactory.register_operation('invalid', BadOperation)
