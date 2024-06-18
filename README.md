[![Beta](https://img.shields.io/badge/Status-Beta-yellow)](https://github.com/FullSnackWebDevClayton/PS5-UART-TOOL)

# PS5 Toolbox

This repository contains the PS5 Toolbox, a utility developed by Tech Centre UK for interacting with PS5 UART connections AND Bios/NOR Modifier.

## Contents

1. [Source Files (src)](#source-files)
2. [Usage](#usage)

---

## Source Files

The directory holds all the source files necessary for building and running the PS5 Toolbox.

## Usage

1. Download pre built packages.
2. Use the build scripts included in source.
3. Build the app manually from src.

To build the PS5 Toolbox:

**Building from Source**: If you want to build the tool from source, navigate to the `src` directory and run the appropriate commands.

### MAC

1. Install Homebrew (if not already installed):
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Install Python 3 using Homebrew:
> brew install python@3.12

3. Create a virtual environment (optional but recommended):
3a. > python3 -m venv myenv
3b. > source myenv/bin/activate

4. Install requirements:
> pip -r install requirements.txt

5. Install Nuitka using pip:
> pip install nuitka

6. Build App with Nuitka:
> python -m nuitka --standalone --macos-create-app-bundle --macos-app-icon=mac.icns main.py

7. Say yes too all prompts to download.

8. You will find the app in the workign directory when complete.

### Windows

1. Check if python is installed:
> python3 --version

if Python not installed download from https://www.python.org/downloads/

2. Optional: Set Up a Virtual Environment (Recommended):
2a. > python -m venv myenv
2b. > myenv\Scripts\activate

3. Install requirements:
> pip -r install requirements.txt

4. Install Nuitka:
> pip install nuitka

5. Build exe:
> python -m nuitka --windows-disable-console --standalone --windows-icon-from-ico=windows.ico PS5-Toolbox.py

6. Say yes to all prompts to download.

7. you will find a folder called PS5-Toolbox.dist, this is all the files needed to run the exe file in the same folder.


## Console Repair Wiki

We also maintain a [Console Repair Wiki](http://www.consolerepair.wiki/) where users can submit codes, updates to code descriptions, create guides, and tutorials to help others in the community. It's a collaborative platform aimed at creating a network of information to assist console repair enthusiasts. If you can contribute, Please do!
