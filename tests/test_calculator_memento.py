import datetime

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento

def test_memento_to_dict():

    # Test Memento to_dict

    memento = CalculatorMemento(
        history = [
            Calculation('Percentage', 3, 5),
            Calculation('AbsoluteDifference', 5, 8),
        ],
    )

    actual = memento.to_dict()
    del(actual['timestamp'])
    for row in actual['history']:
        del(row['timestamp'])

    assert actual == {
        'history': [
            {
                'operation': 'Percentage',
                'operand1': '3',
                'operand2': '5',
                'result': '60.0',
            },
            {
                'operation': 'AbsoluteDifference',
                'operand1': '5',
                'operand2': '8',
                'result': '3',
            }
        ]
    }

def test_memento_from_dict():

    # Test Memento from_dict

    data = {
        'history': [
            {
                'operation': 'IntegerDivision',
                'operand1': '12',
                'operand2': '5',
                'result': '2',
                'timestamp': datetime.datetime.now().isoformat(),
            },
            {
                'operation': 'Modulus',
                'operand1': '9',
                'operand2': '4',
                'result': '1',
                'timestamp': datetime.datetime.now().isoformat(),
            }
        ],
        'timestamp': datetime.datetime.now().isoformat(),
    }

    actual = CalculatorMemento.from_dict(data)
    actual.history = [calc.to_dict() for calc in actual.history]
    assert actual.history == data['history']
    assert actual.timestamp.isoformat() == data['timestamp']
