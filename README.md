[![Beta](https://img.shields.io/badge/Status-Beta-yellow)](https://github.com/FullSnackWebDevClayton/PS5-UART-TOOL)

# PS5 Toolbox

This repository contains the PS5 Toolbox, a utility developed by Tech Centre UK for interacting with PS5 UART connections AND Bios/NOR Modifier.

## Usage

1. Download pre built packages.

OR

2. Build the app manually from Source.


### MAC

Intel and Apple silicone use the same app (you can use either)

Older Apple devices use the MAC-10.9-UNIVERSAL2 version.

### Windows

WINDOWS-10-11 version has been tested on 10 and 11 but will likely work on older.


## Source Files

The directory holds all the source files necessary for building and running the PS5 Toolbox.

### To build the PS5 Toolbox:
''' If you are building from source you should already know the commands else you have no reason to be building from source. '''
**Building from Source**: 
1. Install Virutal ENV
2. Install requirements.txt
#### Mac
3. py2app for mac: pip setup.py PS5-Toolbox.py
#### Windows
3. pyinstaller for windows: pyinstaller --onefile --windowed --icon=windows.ico PS5-Toolbox.py

## Console Repair Wiki

We also maintain a [Console Repair Wiki](http://www.consolerepair.wiki/) where users can submit codes, updates to code descriptions, create guides, and tutorials to help others in the community. It's a collaborative platform aimed at creating a network of information to assist console repair enthusiasts. If you can contribute, Please do!


MIT License

Copyright (c) 2024 Tech Centre UK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
