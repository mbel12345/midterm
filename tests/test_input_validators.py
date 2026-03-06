import pytest

from decimal import Decimal

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

# Config that is used by the validator during testing
config = CalculatorConfig(max_input_value=Decimal('10000'))

def test_validate_positive_integer():

    assert InputValidator.validate_number(1234, config) == Decimal('1234')

def test_validate_positive_decimal():

    assert InputValidator.validate_number(1234.56, config) == Decimal('1234.56').normalize()

def test_validate_positive_string_integer():

    assert InputValidator.validate_number('1234', config) == Decimal('1234')

def test_validate_positive_string_decimal():

    assert InputValidator.validate_number('1234.56', config) == Decimal('1234.56').normalize()

def test_validate_negative_integer():

    assert InputValidator.validate_number(-123, config) == Decimal('-123')

def test_validate_negative_decimal():

    assert InputValidator.validate_number(-123.456, config) == Decimal('-123.456').normalize()

def test_validate_negative_string_integer():

    assert InputValidator.validate_number('-123', config) == Decimal('-123')

def test_validate_number_negative_string_decimal():

    assert InputValidator.validate_number('-123.456', config) == Decimal('-123.456').normalize()

def test_validate_zero():

    assert InputValidator.validate_number(0, config) == Decimal('0')

def test_validate_trimmed_string():

    assert InputValidator.validate_number('  4567      ', config) == Decimal('4567')

def test_validate_invalid_string():

    with pytest.raises(ValidationError, match='Invalid number format: xyz'):
        InputValidator.validate_number('xyz', config)

def test_validate_exceeds_max_value():

    with pytest.raises(ValidationError, match='Value exceeds maximum allowed'):
        InputValidator.validate_number(Decimal('10001'), config)

def test_validate_exceeds_negative_max_value():

    with pytest.raises(ValidationError, match='Value exceeds maximum allowed'):
        InputValidator.validate_number(-Decimal('10001'), config)

def test_validate_empty_string():

    with pytest.raises(ValidationError, match='Invalid number format: '):
        InputValidator.validate_number('', config)

def test_validate_whitespace_string():

    with pytest.raises(ValidationError, match='Invalid number format: '):
        InputValidator.validate_number('   \t', config)

def test_validate_none_value():

    with pytest.raises(ValidationError, match='Invalid number format: None'):
        InputValidator.validate_number(None, config)

def test_validate_non_numeric_type():

    with pytest.raises(ValidationError, match='Invalid number format: '):
        InputValidator.validate_number({}, config)
