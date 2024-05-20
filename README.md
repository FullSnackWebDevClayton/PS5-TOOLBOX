# PS5 UART Tool

This repository contains the PS5 UART Tool, a utility developed by Tech Centre UK for interacting with PS5 UART connections.

## Contents

1. [Source Files (src)](#source-files)
2. [Pre-built macOS ARM64 Example](#pre-built-macos-arm64-example)
3. [Pre-built Windows x64](#pre-built-windows-x64)
4. [Usage](#usage)

---

## Source Files

The `src` directory holds all the source files necessary for building and running the PS5 UART Tool. It includes the following files:

- `build.bat`: Batch script for building the Windows executable and installer.
- `build.sh`: Shell script for building the macOS executable and installer.
- `requirements.txt`: List of Python dependencies required by the tool.
- `mac-setup.py`: Script for creating the macOS installer.
- `windows-setup.py`: Script for creating the Windows installer.
- Other source files and scripts necessary for the functionality of the tool.

## Pre-built macOS ARM64 Example

The `MacOSX_ARM64` directory contains an example build of the PS5 UART Tool for macOS ARM64 architecture. It includes the executable file (`exe.macosx-14.0-arm64-3.12`) and any additional resources required for running the tool on macOS ARM64 systems.

## Pre-built Windows x64

The `Windows_amd64` directory contains pre-built versions of the PS5 UART Tool for Windows x64 architecture. It includes both a portable version and an installer version (`Win-Installer v0.0.1`, `Win-Portable v0.0.1`), allowing users to choose the installation method that suits their needs.

## Usage

To use the PS5 UART Tool:

1. **Windows**: Navigate to the `Windows_amd64` directory and choose between the installer version (`Win-Installer v0.0.1`) or the portable version (`Win-Portable v0.0.1`). Run the appropriate executable file to install or run the tool.

2. **macOS**: Navigate to the `MacOSX_ARM64` directory and run the app OR executable file in (`exe.macosx-14.0-arm64-3.12`) to use the PS5 UART Tool on macOS ARM64 systems. Please note this is only for a specific version of macOS (check step 3 if this does not work for you).

3. **Building from Source**: If you want to build the tool from source, navigate to the `src` directory and run the appropriate build script (`build.bat` for Windows, `build.sh` for macOS). The scripts will install everything needed including dependencies.


## Console Repair Wiki

We also maintain a [Console Repair Wiki](http://www.consolerepair.wiki/) where users can submit codes, updates to code descriptions, create guides, and tutorials to help others in the community. It's a collaborative platform aimed at creating a network of information to assist console repair enthusiasts. If you can contribute, Please do!
