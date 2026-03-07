from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict

from app.exceptions import ValidationError

class Operation(ABC):

    '''
    Abstract base class for calculator operations. Each operation will inherit from this.
    '''

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Do the operation on a and b, and return the result.

        pass # pragma: no cover

    @abstractmethod
    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        # Validate the operands, for example that b is not a 0 for the division operation.

        pass # pragma: no cover

    def __str__(self) -> str:

        # Nice string representation of a calculation

        return self.__class__.__name__

class OperationFactory:

    # Factory for creating Operations

    _operations: Dict[str, type] = {}

    @classmethod
    def register_operation(cls, operation_type: str) -> None:

        def decorator(subclass):

            if not issubclass(subclass, Operation):
                raise TypeError('Class must inherit from Operation')
            # Check if the operation type has already been registered to avoid duplication.
            if operation_type.lower() in cls._operations:
                raise ValueError(f"Operation type '{operation_type.lower()}' is already registered.")
            # Register the subclass in the _operations dictionary.
            cls._operations[operation_type.lower()] = subclass
            return subclass  # Return the subclass for chaining or additional use.

        return decorator

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:

        # Return a new instance of an Operation corresponding to operation_type

        operation_class = cls._operations.get(operation_type.lower())

        if not operation_class:
            raise ValueError(f'Unknown operation: {operation_type}')

        return operation_class()

@OperationFactory.register_operation('add')
class Addition(Operation):

    # Add operation

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Add a and b

        self.validate_operands(a, b)
        return a + b

    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        # Any numbers are valid

        return

@OperationFactory.register_operation('subtract')
class Subtraction(Operation):

    # Subtract operation

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Subtract a and b

        self.validate_operands(a, b)
        return a - b

    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        # Any numbers are valid

        return

@OperationFactory.register_operation('multiply')
class Multiplication(Operation):

    # Multiply operation

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Multiply a and b

        self.validate_operands(a, b)
        return a * b

    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        # Any numbers are valid

        return

@OperationFactory.register_operation('divide')
class Division(Operation):

    # Divide operation

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Divide a and b

        self.validate_operands(a, b)
        return a / b

    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        # Cannot divide by 0

        if b == 0:
            raise ValidationError('Division by zero is not allowed')

@OperationFactory.register_operation('power')
class Power(Operation):

    # Exponent operation

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Compute a raised to b

        self.validate_operands(a, b)
        return a ** b

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # Do not support negative exponents (use root instead)
        if b < 0:
            raise ValidationError('Negative exponents not supported')

@OperationFactory.register_operation('root')
class Root(Operation):

    # Root operation (inverse of Power)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Compute a raised to 1/b, for example, use b=2 to find the square root

        self.validate_operands(a, b)
        return a ** (1/b)

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # Cannot compute the roots of negative numbers, cannot compute 0 roots

        if a < 0:
            raise ValidationError('Cannot calculate root of negative number')

        if b == 0:
            raise ValidationError('Zero root is undefined')

@OperationFactory.register_operation('modulus')
class Modulus(Operation):

    # Modulus operation (% i.e. remainder)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Compute a % b

        self.validate_operands(a, b)
        return a % b

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # Any numbers are valid

        pass

@OperationFactory.register_operation('int_divide')
class IntegerDivision(Operation):

    # Integer division (//)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Compute a // b

        self.validate_operands(a, b)
        return a // b

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # Any numbers are valid

        pass

@OperationFactory.register_operation('percent')
class Percentage(Operation):

    # Calculate the percentage of one number (a) with respect to b.
    # For example, if a=1.5, b=2: result=75.

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Calculate the percentage of a with respect with b

        self.validate_operands(a, b)
        return (a / b)*100

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # a must be non-negative, b must be greater than 0

        if b == 0:
            raise ValidationError('Cannot calculate percentages when b (denominator) is 0')

        if a < 0 or b < 0:
            raise ValidationError('Cannot calculate percentages involving negative numbers')

@OperationFactory.register_operation('abs_diff')
class AbsoluteDifference(Operation):

    # Absolute value of the difference between a and b i.e abs(a - b)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:

        # Absolute value of the difference between a and b i.e abs(a - b)

        self.validate_operands(a, b)
        return abs(a - b)

    def validate_operands(self, a: Decimal, b: Decimal) -> Decimal:

        # Any numbers are valid

        pass

