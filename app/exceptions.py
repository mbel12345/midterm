class CalculationError(Exception):

    '''
    Base class for all other custom errors for the calculator
    '''

    pass

class ValidationError(CalculationError):

    '''
    Raised when input validation fails
    '''

    pass
