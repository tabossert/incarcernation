# incarcernation
https://incarcernation.com/

This repo contains a tools to process articles from incarcernation.com and extract the key details into a structured format for the website database.

# Installing Python and Running Programs
Python must be 3.11 or higher.

## Installing Python on Windows

1. Visit the official Python website: https://www.python.org/downloads/windows/
2. Download the latest Python installer for Windows
3. Run the installer
4. Check "Add Python to PATH" during installation
5. Click "Install Now"

## Installing Python on Mac

1. Open Terminal
2. Install Homebrew if not already installed:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
3. Install Python using Homebrew:
```
brew install python
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
