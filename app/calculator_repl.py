from colorama import Fore
from colorama import init as colorama_init

from app.calculation import Calculation
from app.calculator import Calculator
from app.exceptions import OperationError
from app.exceptions import ValidationError
from app.history import AutoSaveObserver
from app.history import LoggingObserver
from app.logger import Logger
from app.operations import OperationFactory

'''
REPL calculator that can perform Add, Subtract, Multiply, Divide, Power, Root, Modulus, Integer Divide, Percentage, and Absolute Difference.
Stores history and logs all operations.
'''

def calculator_repl():

    try:

        colorama_init()

        calc = Calculator()

        # Register observers
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(Fore.MAGENTA + 'Calculator started. Type \'help\' for commands')

        while True:

            try:

                command = input(Fore.LIGHTBLUE_EX + '\nEnter command: ').lower().strip()

                if command == 'help':
                    # Display allowed commands
                    # Operations taken from the Decorator registration in OperationFactory
                    print(Fore.CYAN + '\nAvailable commands:')
                    print(f'{Fore.CYAN}  {', '.join(OperationFactory._operations.keys())} - Perform calculations')
                    print(f'{Fore.CYAN}  history - Show calculation history')
                    print(f'{Fore.CYAN}  clear - Clear calculation history')
                    print(f'{Fore.CYAN}  undo - Undo the last calculation')
                    print(f'{Fore.CYAN}  redo - Redo the last undone calculation')
                    print(f'{Fore.CYAN}  save - Save calculation history to file')
                    print(f'{Fore.CYAN}  load - Load calculation history from file')
                    print(f'{Fore.CYAN}  exit - Exit the calculator')
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print(Fore.GREEN + 'History saved successfully')
                    except Exception as e:
                        print(f'{Fore.YELLOW}Warning: Could not save history: {e}')
                    print(Fore.MAGENTA + 'Goodbye!')
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(Fore.YELLOW + 'No calculations in history')
                    else:
                        print(Fore.CYAN + '\nCalculation History:')
                        for i, entry in enumerate(history, 1):
                            print(f'{Fore.CYAN}{i}. {entry}')
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(Fore.GREEN + 'History cleared')
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(Fore.GREEN + 'Operation undone')
                    else:
                        print(Fore.YELLOW + 'Nothing to undo')
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(Fore.GREEN + 'Operation redone')
                    else:
                        print(Fore.YELLOW + 'Nothing to redo')
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(Fore.GREEN + 'History saved successfully')
                    except Exception as e:
                        print(f'{Fore.RED}Error saving history: {e}')
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(Fore.GREEN + 'History loaded successfully')
                    except Exception as e:
                        print(f'{Fore.RED}Error loading history: {e}')
                    continue

                if command in OperationFactory._operations:
                    try:
                        print(Fore.LIGHTBLUE_EX + "\nEnter numbers (or 'cancel'; to abort):")
                        a = input('First number: ')
                        if a.lower() == 'cancel':
                            print(Fore.YELLOW + 'Operation cancelled')
                            continue
                        b = input('Second number: ')
                        if b.lower() == 'cancel':
                            print(Fore.YELLOW + 'Operation cancelled')
                            continue

                        # Create the appropriate operation using a Factory
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        print(f'{Fore.GREEN}\nResult: {Calculation.format_result(result)}')

                    except (ValidationError, OperationError) as e:
                        print(f'{Fore.RED}Error: {e}')

                    except Exception as e:
                        print(f'{Fore.RED}Unexpected error: {e}')

                    continue

                print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print(Fore.YELLOW + '\nOperation cancelled')

            except EOFError:
                print(Fore.YELLOW + '\nInput terminated. Exiting...')

            except Exception as e:
                print(f'{Fore.RED}Error: {e}')
                continue

    except Exception as e:

        # Fatal errors

        print(f'{Fore.RED}Fatal error: {e}')
        Logger.error(f'{Fore.RED}Fatal error in calculator REPL: {e}')
