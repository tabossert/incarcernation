# incarcernation
https://incarcernation.com/

This repo contains a tools to process articles from incarcernation.com and extract the key details into a structured format for the website database.

# Clone repo
```
git clone https://github.com/tabossert/incarcernation/
```

If you don't have git you can download the files manually, but git is preferred.

# Installing Python and Running Programs
Python version must be 3.10, 3.11, or 3.12.

## Installing Python on Windows

1. Download the 3.12 Python installer for Windows https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
2. Run the installer
3. Check "Add Python to PATH" during installation
4. Click "Install Now"

## Installing Python on Mac

1. Open Terminal
2. Install Homebrew if not already installed:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
3. Install Python using Homebrew:
```
brew install python@3.12
```

## Installing pip Requirements
If you prefer you can create a virtual environment to run the program in, but it is not required.

1. Navigate to the directory article-processor which contains the requirements.txt file
2. Run the following command:
```
pip install -r requirements.txt
```

## Running a Python Program

1. Navigate to the directory article-processor
2. Run the following command:
```
python article_processer.py
```
