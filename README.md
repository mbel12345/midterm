# Project Summary

This is a REPL (read-evaluate-print-loop) calculator that performs various operations requested by the user. The user enters an operation, a number, and another number, and then sees the result. The operations are (with examples of what the user should enter):
  - Addition: add, 4, 5 = 9
  - Subtraction: subtract, 4, 3 = 1
  - Multiplication: multiply, 4, 7 = 28
  - Division: divide, 6, 4 = 1.5
  - Power (exponent): power, 3, 2 = 9
  - Root: root, 9, 2 = 3
  - Modulus (remainder): modulus, 7, 3 = 1
  - Integer Division (truncate the decimal point after division): int_divide, 6, 4 = 1
  - Percentage (percentage of number 1 vs. number 2): percent, 4, 5 = 80
  - Absolute Difference (absolute value after subtraction): abs_diff, 4, 7 = 3

Other calculator options are:
  - history – Display calculation history.
  - clear – Clear calculation history.
  - undo – Undo the last calculation.
  - redo – Redo the last undone calculation.
  - save – Manually save calculation history to file using pandas.
  - load – Load calculation history from file using pandas.
  - help – Display available commands.
  - exit – Exit the application gracefully.

## Logging and History
All operations are logged to history/calculator_history.csv by default (overwritable with CALCULATOR_HISTORY_FILE environment var).
All logs for the application are logged to logs/calculator.log by default (overwritable with LOG_FILE environment var).
Operations can be undone or redone because the history is also saved to memory and can be loaded from the history file.

## Github Actions
Whenever a new branch is pushed to git, or a branch is merged into main, Github Actions run to validate that all test cases pass and that there is 100% test coverage. My workflow for this project is to do all work in a feature branch, and then merge to main whenever fully tested - with Github Actions giving me a clear indication if there are any problems with the application during this process.

# Project Setup and Usage

## Set up Repo
In Github:
Create new repo called midterm and make sure it is public

In WSL/VS Code Terminal:
```bash
mkdir midterm
cd midterm/
git init
git branch -m main
git remote add origin git@github.com:mbel12345/midterm.git
vim README.md
git add . -v
git commit -m "Initial commit"
git push -u origin main
```

## Set up virtual environment
In WSL/VS Code Terminal:
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run test cases
In WSL/VS Code Terminal:
```bash
pytest
```

You should see something like below, with the last column showing that coverage is 100% and the last showing that all tests passed:

```
---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                        Stmts   Miss Branch BrPart  Cover   Missing
app/__init__.py                 0      0      0      0   100%
app/calculation.py             61      0      6      0   100%
app/calculator.py             126      0     22      0   100%
app/calculator_config.py       41      0      6      0   100%
app/calculator_memento.py      13      0      0      0   100%
app/exceptions.py               8      0      0      0   100%
app/history.py                 23      0      8      0   100%
app/input_validators.py        18      0      4      0   100%
app/logger.py                  14      0      0      0   100%
app/operations.py              92      0     16      0   100%
-----------------------------------------------------------------------
TOTAL                         396      0     62      0   100%
Coverage HTML written to dir htmlcov

144 passed in 1.84s 
```

## Run the calculator
In WSL/VS Code Terminal:
```bash
python3 main.py
```

## Configuration
These are the environment vars that can be configured to alter program behavior:<br/>
  - CALCULATOR_LOG_DIR: Directory for log files.
  - CALCULATOR_LOG_FILE: Log file.
  - CALCULATOR_HISTORY_DIR: Directory for history files.
  - CALCULATOR_HISTORY_FILE: History file.
  - CALCULATOR_MAX_HISTORY_SIZE: Maximum number of history entries.
  - CALCULATOR_AUTO_SAVE: Whether to auto-save history (true or false).
  - CALCULATOR_PRECISION: Number of decimal places for calculations.
  - CALCULATOR_MAX_INPUT_VALUE: Maximum allowed input value.
  - CALCULATOR_DEFAULT_ENCODING: Default encoding for file operations.

## dotenv file
At the project root (midterm/.env), you can provide vars that override the defaults. Example .env file:<br/>
CALCULATOR_LOG_DIR=./logs_dotenv<br/>
CALCULATOR_LOG_FILE=./logs_dotenv/log_test.log<br/>
CALCULATOR_HISTORY_DIR=./history_dotenv<br/>
CALCULATOR_HISTORY_FILE=./history_dotenv/history_test.csv<br/>
CALCULATOR_MAX_HISTORY_SIZE=200<br/>
CALCULATOR_AUTO_SAVE=false<br/>
CALCULATOR_PRECISION=4<br/>
CALCULATOR_MAX_INPUT_VALUE=1000<br/>
CALCULATOR_DEFAULT_ENCODING=ascii<br>
