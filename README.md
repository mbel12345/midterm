# Project Setup

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

## Run the calculator
In WSL/VS Code Terminal:
```bash
python3 main.py
```
