import logging
import pytest
import re

from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.calculation import Calculation
from app.exceptions import OperationError

class BaseCalculationTest:

    '''
    Use this class to facilitate parameterized testing, intead of the lengthy pytest.mark.parametrize. This also allows testing to be standardized across sub-classes.
    '''

    def test_valid_calcs(self):

        # Test calculation with valid inputs

        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected = Decimal(str(case['expected']))
            calc = Calculation(operation=self.operation, operand1=a, operand2=b)
            assert calc.result == expected, f'Failed case: {name}'

    def test_invalid_calcs(self):

        # Test calculations with invalid inputs, and verify the correct errors were raised

        for _, case in self.invalid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected_error = case['error']
            expected_message = case['message']
            with pytest.raises(expected_error, match=expected_message):
                calc = Calculation(operation=self.operation, operand1=a, operand2=b)

class TestAdditionCalculation(BaseCalculationTest):

    # Test Add calculation

    operation = 'Addition'
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '8'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '-8'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-2'},
        'zero_sum': {'a': '5', 'b': '-5', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '8.8'},
        'large_numbers': {'a': '1e10', 'b': '1e10', 'expected': '20000000000'},
    }
    invalid_test_cases = {}

class TestSubtractionCalculation(BaseCalculationTest):

    # Test Subtract calculation

    operation = 'Subtraction'
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '2'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '-2'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-8'},
        'zero_result': {'a': '5', 'b': '5', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '2.2'},
        'large_numbers': {'a': '1e10', 'b': '1e9', 'expected': '9000000000'},
    }
    invalid_test_cases = {}

class TestMultiplicationCalculation(BaseCalculationTest):

    # Test Multiply calculation

    operation = 'Multiplication'
    valid_test_cases = {
        'positive_numbers': {'a': '5', 'b': '3', 'expected': '15'},
        'negative_numbers': {'a': '-5', 'b': '-3', 'expected': '15'},
        'mixed_signs': {'a': '-5', 'b': '3', 'expected': '-15'},
        'multiply_by_zero': {'a': '5', 'b': '0', 'expected': '0'},
        'decimals': {'a': '5.5', 'b': '3.3', 'expected': '18.15'},
        'large_numbers': {'a': '1e5', 'b': '1e5', 'expected': '10000000000'},
    }
    invalid_test_cases = {}

class TestDivisionCalculation(BaseCalculationTest):

    # Test Divide calculation

    operation = 'Division'
    valid_test_cases = {
        'positive_numbers': {'a': '6', 'b': '2', 'expected': '3'},
        'negative_numbers': {'a': '-6', 'b': '-2', 'expected': '3'},
        'mixed_signs': {'a': '-6', 'b': '2', 'expected': '-3'},
        'decimals': {'a': '5.5', 'b': '2', 'expected': '2.75'},
        'divide_zero': {'a': '0', 'b': '5', 'expected': '0'},
    }
    invalid_test_cases = {
        'divide_by_zero': {'a': '5', 'b': '0', 'error': OperationError, 'message': 'Division by zero is not allowed'},
    }

class TestPowerCalculation(BaseCalculationTest):

    # Test Power calculation

    operation = 'Power'
    valid_test_cases = {
        'positive_base_and_exponent': {'a': '2', 'b': '3', 'expected': '8'},
        'zero_exponent': {'a': '5', 'b': '0', 'expected': '1'},
        'one_exponent': {'a': '5', 'b': '1', 'expected': '5'},
        'decimal_base': {'a': '2.5', 'b': '2', 'expected': '6.25'},
        'zero_base': {'a': '0', 'b': '5', 'expected': '0'},
    }
    invalid_test_cases = {
        'negative_exponent': {'a': '2', 'b': '-3', 'error': OperationError, 'message': 'Negative exponents not supported'},
    }

class TestRootCalculation(BaseCalculationTest):

    # Test Root calculation

    operation = 'Root'
    valid_test_cases = {
        'square_root': {'a': '9', 'b': '2', 'expected': '3'},
        'cube_root':  {'a': '27', 'b': '3', 'expected': '3'},
        'fourth_root':  {'a': '16', 'b': '4', 'expected': '2'},
        'decimal_root': {'a': '2.25', 'b': '2', 'expected': '1.5'},
    }
    invalid_test_cases = {
        'negative_base': {'a': '-9', 'b': '2', 'error': OperationError, 'message': 'Cannot calculate root of negative number'},
        'zero_root': {'a': '9', 'b': '0', 'error': OperationError, 'message': 'Zero root is undefined'},
    }

class TestModulusCalculation(BaseCalculationTest):

    # Test Modulus calculation

    operation = 'Modulus'
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

class TestIntegerDivisionCalculation(BaseCalculationTest):

    # Test Integer Divide calculation

    operation = 'IntegerDivision'
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

class TestPercentageCalculation(BaseCalculationTest):

    # Test Percentage calculation

    operation = 'Percentage'
    valid_test_cases = {
        'positive_integers': {'a': '10', 'b': '50', 'expected': '20'},
        'positive_floats': {'a': '4.5', 'b': '10', 'expected': '45'},
        'mixed_numbers': {'a': '0.005', 'b': '2.5', 'expected': '0.2'},
        'large_numbers': {'a': '1e9', 'b': '1e10', 'expected': '10'},
    }
    invalid_test_cases = {
        'negative_integer_and_positive_integer': {'a': '-5', 'b': '100', 'error': OperationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'positive_integer_and_negative_integer': {'a': '5', 'b': '-100', 'error': OperationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'negative_integers': {'a': '-5', 'b': '-100', 'error': OperationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'negative_floats': {'a': '-5.5', 'b': '-1.5', 'error': OperationError, 'message': 'Cannot calculate percentages involving negative numbers'},
        'zero_denominator': {'a': '-5.5', 'b': '0', 'error': OperationError, 'message': 'Cannot calculate percentages when b \\(denominator\\) is 0'},
    }

class TestAbsoluteDifferenceCalculation(BaseCalculationTest):

    # Test Absolute Difference calculation

    operation = 'AbsoluteDifference'
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

def test_unknown_operation():

    # Check for unknown operation error

    with pytest.raises(OperationError, match='Unknown operation'):
        Calculation(operation='Unknown', operand1=Decimal('5'), operand2=Decimal('3'))

def test_to_dict():

    # Test converting a Calculator to dict

    calc = Calculation(operation='Addition', operand1=Decimal('2'), operand2=Decimal('3'))
    result_dict = calc.to_dict()
    assert result_dict == {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '5',
        'timestamp': calc.timestamp.isoformat(),
    }

def test_from_dict():

    # Test loading a Calculator from dict

    data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '5',
        'timestamp': datetime.now().isoformat()
    }

    calc = Calculation.from_dict(data)
    assert calc.operation == 'Addition'
    assert calc.operand1 == Decimal('2')
    assert calc.operand2 == Decimal('3')
    assert calc.result == Decimal('5')

def test_invalid_from_dict():

    # Test failure to load a Calculator from dict

    data = {
        'operation': 'Addition',
        'operand1': 'invalid',
        'operand2': '3',
        'result': '5',
        'timestamp': datetime.now().isoformat(),
    }

    with pytest.raises(OperationError, match='Invalid calculation data'):
        Calculation.from_dict(data)

def test_format_result():

    # Test using the right precision in decimal numbers

    calc = Calculation(operation='Division', operand1=Decimal('1'), operand2=Decimal('3'))
    assert Calculation.format_result(result=calc.result, precision=2) == '0.33'
    assert Calculation.format_result(result=calc.result, precision=10) == '0.3333333333'

def test_format_result_trailing_zeros():

    calc = Calculation(operation='Percentage', operand1=Decimal('2'), operand2=Decimal('5'))
    assert Calculation.format_result(calc.result) == '40'

def test_format_result_float():

    calc = Calculation(operation='Addition', operand1=Decimal('0'), operand2=Decimal('0'))
    calc.result = 45.5
    assert Calculation.format_result(calc.result) == '45.5'

def test_equality():

    # Test comparison between Calculators

    calc_1 = Calculation(operation='Addition', operand1=Decimal('2'), operand2=Decimal('3'))
    calc_2 = Calculation(operation='Addition', operand1=Decimal('2'), operand2=Decimal('3'))
    calc_3 = Calculation(operation='Subtraction', operand1=Decimal('5'), operand2=Decimal('3'))

    assert calc_1 == calc_2
    assert calc_1 != calc_3

def test_from_dict_result_mismatch(caplog):

    # Check logging warning

    data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '10',
        'timestamp': datetime.now().isoformat(),
    }

    with caplog.at_level(logging.WARNING):
        Calculation.from_dict(data)

    assert 'Loaded calculation result 10 differs from computed result 5' in caplog.text

'''
Cases beyond the instructor-posted code, to ensure full coverage
'''

def test_calculate_arithmetic_error(monkeypatch):

    # Test unexpected Arithmetic error

    class BadDecimal(Decimal):
        def __truediv__(self, other):
            raise ArithmeticError('force failure')

    import app.calculation as calc_mod
    monkeypatch.setattr(calc_mod, 'Decimal', BadDecimal)

    with pytest.raises(OperationError, match='Calculation failed: force failure'):
        Calculation(operation='Division', operand1=BadDecimal('5'), operand2=BadDecimal('2'))

def test_calculation_str():

    # Test __str__ method

    calc = Calculation(operation='Addition', operand1=Decimal('4'), operand2=Decimal('2'))
    assert str(calc) == 'Addition(4, 2) = 6'

def test_calculation_repr():

    # Test __repr__ method

    calc = Calculation(operation='Addition', operand1=Decimal('3'), operand2=Decimal('2'))
    assert re.match("Calculation\\(operation='Addition', operand1=3, operand2=2, result=5, timestamp=.*\\)", repr(calc))

def test_equals_wrong_types():

    # Check that an error is thrown in __eq__ when comparing a Calculation to a non-Calculation

    calc = Calculation(operation='Addition', operand1=Decimal('0'), operand2=Decimal('0'))
    assert calc.__eq__(0) == NotImplemented

def test_format_result_error(monkeypatch):

    # Test error during formatting

    class BadResult:

        def __init__(self, x):

            self.x = x

        def __str__(self):

            return str(self.x)

        def normalize(self):
            raise InvalidOperation('force formatting failure')

    calc = Calculation(operation='Addition', operand1=Decimal('5'), operand2=Decimal('2'))
    calc.result = BadResult('34')
    assert Calculation.format_result(calc.result) == '34'

