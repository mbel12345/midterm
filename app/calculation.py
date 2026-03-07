import datetime
import numbers
import re

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Dict

from app.exceptions import OperationError
from app.exceptions import ValidationError
from app.logger import Logger
from app.operations import AbsoluteDifference
from app.operations import Addition
from app.operations import Division
from app.operations import IntegerDivision
from app.operations import Modulus
from app.operations import Multiplication
from app.operations import Percentage
from app.operations import Power
from app.operations import Root
from app.operations import Subtraction

@dataclass
class Calculation:

    '''
    This class encapsulates the details of a mathematical calculation,
    including the operation name, two nubmers, result, and timestamp.
    '''

    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):

        # Takes place after the default __init__ method for dataclass that initiates all the values

        self.result = self.calculate()

    def calculate(self) -> Decimal:

        # Do the calculation.

        operations = {
            'Addition': lambda x, y: Addition().execute(x, y),
            'Subtraction': lambda x, y: Subtraction().execute(x, y),
            'Multiplication': lambda x, y: Multiplication().execute(x, y),
            'Division': lambda x, y: Division().execute(x, y),
            'Power': lambda x, y: Power().execute(x, y),
            'Root': lambda x, y: Root().execute(x, y),
            'Modulus': lambda x, y: Modulus().execute(x, y),
            'IntegerDivision': lambda x, y: IntegerDivision().execute(x, y),
            'Percentage': lambda x, y: Percentage().execute(x, y),
            'AbsoluteDifference': lambda x, y: AbsoluteDifference().execute(x, y),
        }

        # Get the operation from the dict based on operation name
        op = operations.get(self.operation)
        if not op:
            raise OperationError(f'Unknown operation: {self.operation}')

        try:

            return op(self.operand1, self.operand2)

        except (ArithmeticError, InvalidOperation, ValidationError, ValueError, ) as e:

            raise OperationError(f'Calculation failed: {str(e)}')

    def to_dict(self) -> Dict[str, Any]:

        # Convert to dict showing most important info like operation and operands

        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': Calculation.format_result(self.result),
            'timestamp': self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':

        # Create calculation from dictionary

        try:

            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2']),
            )

            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                Logger.warning(
                    f'Loaded calculation result {saved_result} '
                    f'differs from computed result {calc.result}'
                )

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:

            raise OperationError(f'Invalid calculation data: {str(e)}')

    def __str__(self) -> str:

        # Return str representation of the calculation

        return f'{self.operation}({self.operand1}, {self.operand2}) = {self.result}'

    def __repr__(self) -> str:

        # Return detailed str representation of the calculation

        return (
            f"Calculation(operation='{self.operation}', "
            f'operand1={self.operand1}, '
            f'operand2={self.operand2}, '
            f'result={self.result}, '
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:

        # Check if two calculations are equal

        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )

    # Static method since this method needs to be called against str objects directly when no Calculation object is being used, like in calculator_repl.py.
    @staticmethod
    def format_result(result, precision: int = 10) -> str:

        # Format the calculation for the given precision

        try:

            if isinstance(result, numbers.Number):
                result = Decimal(result)

            result = str(
                result.normalize().quantize(
                    Decimal('0.' + '0' * precision)
                ).normalize()
            )

            if 'E' in result:
                result = format(Decimal(result), 'f')

            result = re.sub('(.*\..*)0+$', '\\1', result) # Remove trailing zeros

            return result

        except InvalidOperation:

            return str(result)

