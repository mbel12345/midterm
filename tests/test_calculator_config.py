import os
import pytest

from decimal import Decimal
from pathlib import Path

from app.calculator_config import CalculatorConfig
from app.calculator_config import get_project_root
from app.exceptions import ConfigurationError

def clear_env_vars(*args):

    # Helper function to clear a subset of environment vars

    for var in args:
        os.environ.pop(var, None)

def test_default_configuration():

    # Test default config settings

    config = CalculatorConfig()

    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal('1e999')
    assert config.default_encoding == 'utf-8'
    assert config.log_dir == Path('./logs').resolve()
    assert config.log_file == Path('./logs/calculator.log').resolve()
    assert config.history_dir == Path('./history').resolve()
    assert config.history_file == Path('./history/calculator_history.csv').resolve()

def test_custom_config():

    # Test custom config settings

    config = CalculatorConfig(
        max_history_size=300,
        base_dir=(Path(__file__).parent.parent / '/logs/custom').resolve(),
        auto_save=False,
        precision=5,
        max_input_value=Decimal('300'),
        default_encoding='ascii'
    )

    assert config.max_history_size == 300
    assert config.auto_save is False
    assert config.precision == 5
    assert config.max_input_value == Decimal('300')
    assert config.default_encoding == 'ascii'
    assert config.log_dir == (Path(__file__).parent.parent / '/logs/custom/logs').resolve()
    assert config.log_file == (Path(__file__).parent.parent / '/logs/custom/logs/calculator.log').resolve()
    assert config.history_dir == (Path(__file__).parent.parent / '/logs/custom/history').resolve()
    assert config.history_file == (Path(__file__).parent.parent / '/logs/custom/history/calculator_history.csv').resolve()

def test_directory_properties():

    # Check the directory paths

    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()

def test_file_properties():

    # Check the file paths

    clear_env_vars('CALCULATOR_HISTORY_FILE', 'CALCULATOR_LOG_FILE')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.log_file == Path('/custom_base_dir/logs/calculator.log').resolve()
    assert config.history_file == Path('/custom_base_dir/history/calculator_history.csv').resolve()

def test_invalid_max_history_size():

    # Test negative max_history_size

    with pytest.raises(ConfigurationError, match='max_history_size must be positive'):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()

def test_invalid_precision():

    # Test negative precision

    with pytest.raises(ConfigurationError, match='precision must be positive'):
        config = CalculatorConfig(precision=-1)
        config.validate()

def test_invalid_max_input_value():

    # Test negative max_input_value

    with pytest.raises(ConfigurationError, match='max_input_value must be positive'):
        config = CalculatorConfig(max_input_value=-1)
        config.validate()

def test_auto_save_env_var_true():

    # Test setting auto-save

    os.environ['CALCULATOR_AUTO_SAVE'] = 'true'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True

def test_auto_save_env_var_one():

    # Test setting auto-save

    os.environ['CALCULATOR_AUTO_SAVE'] = '1'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True

def test_auto_save_env_var_false():

    # Test setting auto-save

    os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False

def test_auto_save_env_var_zero():

    # Test setting auto-save

    os.environ['CALCULATOR_AUTO_SAVE'] = '0'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False

def test_environment_overrides():

    # Test that environment variables override default settings

    os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '300'
    os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
    os.environ['CALCULATOR_PRECISION'] = '6'
    os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '10000'
    os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'ascii'
    os.environ['CALCULATOR_LOG_DIR'] = './logs_test'
    os.environ['CALCULATOR_LOG_FILE'] = './logs_tmp/log_test.log'
    os.environ['CALCULATOR_HISTORY_DIR'] = './history_test'
    os.environ['CALCULATOR_HISTORY_FILE'] = './history_tmp/history_test.csv'

    config = CalculatorConfig()

    assert config.max_history_size == 300
    assert config.auto_save is False
    assert config.precision == 6
    assert config.max_input_value == Decimal('10000')
    assert config.default_encoding == 'ascii'
    assert config.log_dir == Path('./logs_test').resolve()
    assert config.log_file == Path('./logs_tmp/log_test.log').resolve()
    assert config.history_dir == Path('./history_test').resolve()
    assert config.history_file == Path('./history_tmp/history_test.csv').resolve()

def test_default_fallback():

    # Test that vars fall back if not defined in os.environ

    clear_env_vars('CALCULATOR_MAX_HISTORY_SIZE', 'CALCULATOR_AUTO_SAVE', 'CALCULATOR_PRECISION',
                   'CALCULATOR_MAX_INPUT_VALUE', 'CALCULATOR_DEFAULT_ENCODING',
                   'CALCULATOR_LOG_DIR', 'CALCULATOR_LOG_FILE', 'CALCULATOR_HISTORY_DIR', 'CALCULATOR_HISTORY_FILE')

    config = CalculatorConfig()

    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal('1e999')
    assert config.default_encoding == 'utf-8'
    assert config.log_dir == Path('./logs').resolve()
    assert config.log_file == Path('./logs/calculator.log').resolve()
    assert config.history_dir == Path('./history').resolve()
    assert config.history_file == Path('./history/calculator_history.csv').resolve()

def test_get_project_root():

    # Test that project_root is correct
    assert (get_project_root() / 'app').exists()

def test_log_dir_property():

    # Check that log_dir is valid

    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_LOG_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_dir == Path('/new_base_dir/logs').resolve()

def test_history_dir_property():

    # Check that history_dir is valid

    clear_env_vars('CALCULATOR_HISTORY_DIR', 'CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_dir == Path('/new_base_dir/history').resolve()

def test_log_file_property():

    # Check that log_file is valid

    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_LOG_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_file == Path('/new_base_dir/logs/calculator.log').resolve()

def test_history_file_property():

    # Check that history_FILE is valid

    clear_env_vars('CALCULATOR_HISTORY_DIR', 'CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_file == Path('/new_base_dir/history/calculator_history.csv').resolve()

def test_validate():

    # Make sure that all paths in validate are marked as passed

    config = CalculatorConfig()
    assert config.validate() == None
