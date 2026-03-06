from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@dataclass
class InputValidator:

    '''
    Validate calculator inputs
    '''

    @staticmethod
    def validate_number(v: Any, config: CalculatorConfig) -> Decimal:

        # Validate the number and convert it to Decimal

        try:

            if isinstance(v, str):
                v = v.strip()
            n = Decimal(str(v))
            if abs(n) > config.max_input_value:
                raise ValidationError(f'Value exceeds maximum allowed: {config.max_input_value}')
            return n.normalize()

        except InvalidOperation as e:

            # Error when converting to Decimal object
            raise ValidationError(f'Invalid number format: {v}') from e
