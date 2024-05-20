from cx_Freeze import setup, Executable

# Define build options
build_exe_options = {
    "packages": [
        "os",
        "certifi",
        "charset_normalizer",
        "idna",
        "PIL",
        "serial",
        "requests",
        "six",
        "urllib3",
        "wx",
    ],
    # "include_files": ["ps5controllertcuk.png"],
}

# Call setup function
setup(
    name="PS5 UART Tool",
    version="0.1",
    description="PS5 UART Tool by Tech Centre UK",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui", icon="icon.icns", target_name="PS5_UART_Tool")]
)

# python3 mac-setup.py bdist_mac
