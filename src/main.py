import wx
import serial.tools.list_ports
import serial
import time
import os
import xml.etree.ElementTree as ET
import datetime
import requests
import webbrowser
import binascii

current_date_time = datetime.datetime.now()
formatted_date_time = current_date_time.strftime("%d-%m-%Y %H:%M:%S")
url = "http://198.244.234.174:8001/generate-xml"
tcuk_url = "http://www.consolerepair.wiki/en/submit-uart-code"
donate_url = "https://buymeacoffee.com/techcentreuk"
console_repair_wiki_url = "http://www.consolerepair.wiki"
filename = "error_codes.xml"
download = "http://www.consolerepair.wiki/freshbios.bin"

# Helper functions
def appsupportdir():
    if os.name == 'nt':  # Windows
        appdata = os.getenv('APPDATA')
        return os.path.expandvars(appdata)
    elif os.name == 'posix':  # macOS/Linux
        home = os.path.expanduser('~')
        return os.path.join(home, 'Library', 'Application Support')
    else:
        print("Other")
        return None

def pathinappsupportdir(*paths, create=False):
    location = os.path.join(appsupportdir(), *paths)
    if create:
        os.makedirs(location, exist_ok=True)
    return location

def download_error_codes_xml(url, filename):
    filedir = pathinappsupportdir("PS5_UART_Tool", create=True)
    file_path = os.path.join(filedir, filename)
    try:
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("Downloaded the newest database successfully.")
    except Exception as e:
        print("An error occurred while downloading the newest database:", e)

def save_file_dialog(parent_frame):
    wildcard = "Text files (*.txt)|*.txt"
    dialog = wx.FileDialog(parent_frame, message="Save file", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dialog.ShowModal() == wx.ID_CANCEL:
        return None
    return dialog.GetPath()

class UARTToolFrame(wx.Panel):
    def __init__(self, parent):
        super(UARTToolFrame, self).__init__(parent)
        self.panel = self
        
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        heading_text = wx.StaticText(self.panel, label="\n \nPS5 UART Error Code Tools - BETA v0.1", style=wx.ALIGN_CENTER)
        heading_text.SetFont(font)
        
        heading_margin_top = 20
        heading_text.SetPosition((0, heading_margin_top))
        
        self.port_label = wx.StaticText(self.panel, label="Select Port:")
        self.port_dropdown = wx.ComboBox(self.panel, choices=self.get_available_ports(), style=wx.CB_READONLY)

        self.refresh_button = wx.Button(self.panel, label="Refresh Ports")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh_button_click)
        
        self.action_label = wx.StaticText(self.panel, label="Select Action:")
        self.action_dropdown = wx.ComboBox(self.panel, choices=["Read Error Codes", "Clear Error Codes", "Submit Error Codes", "Custom Command", "Console Repair Wiki", "Exit"], style=wx.CB_READONLY)
        
        self.connect_button = wx.Button(self.panel, label="Start")
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect_button_click)

        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)

        self.clear_button = wx.Button(self.panel, label="Clear Terminal")
        self.clear_button.Bind(wx.EVT_BUTTON, self.on_clear_button_click)

        coffee_emoji = "\U00002615"
        self.donate_button = wx.Button(self.panel, label=f"{coffee_emoji} Buy me a coffee! {coffee_emoji}")
        self.donate_button.Bind(wx.EVT_BUTTON, self.on_donate_button_click)

        vbox_heading = wx.BoxSizer(wx.VERTICAL)
        vbox_heading.Add(heading_text, 0, wx.EXPAND | wx.ALL, 5)

        vbox_port = wx.BoxSizer(wx.HORIZONTAL)
        vbox_port.Add(self.port_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox_port.Add(self.port_dropdown, 1, wx.EXPAND | wx.ALL, 5)
        vbox_port.Add(self.refresh_button, 0, wx.EXPAND | wx.ALL, 5)

        vbox_action = wx.BoxSizer(wx.HORIZONTAL)
        vbox_action.Add(self.action_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox_action.Add(self.action_dropdown, 1, wx.EXPAND | wx.ALL, 5)
        vbox_action.Add(self.connect_button, 0, wx.EXPAND | wx.ALL, 5)

        vbox_text_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        vbox_text_ctrl.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        hbox_buttons.Add(self.clear_button, 0, wx.EXPAND | wx.ALL, 5)
        hbox_buttons.AddStretchSpacer()
        hbox_buttons.Add(self.donate_button, 0, wx.EXPAND | wx.ALL, 5)

        vbox_main = wx.BoxSizer(wx.VERTICAL)
        vbox_main.Add(vbox_heading, 0, wx.EXPAND | wx.ALL, 5)
        vbox_main.Add(vbox_port, 0, wx.EXPAND | wx.ALL, 5)
        vbox_main.Add(vbox_action, 0, wx.EXPAND | wx.ALL, 5)
        vbox_main.Add(vbox_text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        vbox_main.Add(hbox_buttons, 0, wx.EXPAND | wx.ALL, 5)
        
        self.panel.SetSizer(vbox_main)
        self.Show()

        self.text_ctrl.AppendText("Welcome to PS5 UART Tools, by TechCentreUK!\n \n")

    def on_donate_button_click(self, event):
        webbrowser.open(donate_url)

    def on_clear_button_click(self, event):
        self.text_ctrl.Clear()
    
    def get_available_ports(self):
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device + " - " + port.description)
        return ports

    def on_refresh_button_click(self, event):
        self.port_dropdown.Clear()
        self.port_dropdown.AppendItems(self.get_available_ports())
    
    def on_connect_button_click(self, event):
        selected_port_desc = self.port_dropdown.GetValue()
        selected_port = selected_port_desc.split(" - ")[0] if selected_port_desc else ""
        selected_action = self.action_dropdown.GetValue()
        if selected_port:
            self.text_ctrl.AppendText(f"Connecting to port: {selected_port} \n \n")
            if selected_action:
                self.text_ctrl.AppendText(f"Selected action: {selected_action} \n\n")
                if selected_action == "Read Error Codes":
                    self.read_error_codes(selected_port)
                elif selected_action == "Clear Error Codes":
                    self.clear_error_codes(selected_port)
                elif selected_action == "Submit Error Codes":
                    self.submit_error_codes(selected_port)
                elif selected_action == "Custom Command":
                    self.custom_command(selected_port)
                elif selected_action == "Console Repair Wiki":
                    self.open_console_repair_wiki()
                elif selected_action == "Exit":
                    self.Close()
            else:
                self.text_ctrl.AppendText("Please select an action first. \n")
        else:
            self.text_ctrl.AppendText("Please select a port first. \n")
    
    def read_error_codes(self, selected_port):
        try:
            info_dialog = wx.MessageDialog(None, "Reading error codes may take a moment. Please wait... \n", "Reading Error Codes", wx.OK | wx.ICON_INFORMATION)
            if info_dialog.ShowModal() == wx.ID_OK:
                info_dialog.Destroy()
                with serial.Serial(selected_port) as ser:
                    ser.baudrate = 115200
                    ser.rts = True
                    ser.timeout = 5.0
                    errors = False
                    no_error = False
                    self.text_ctrl.AppendText(f"Selected port: {selected_port}\n \nGetting error logs...\n \n")
                    
                    error_codes = self.parse_error_codes(os.path.join(pathinappsupportdir("PS5_UART_Tool"), filename))
                    UARTLines = []

                    for i in range(20):
                        command = f"errlog {i}"
                        checksum = self.calculate_checksum(command)
                        ser.write((checksum + "\n").encode())

                        time.sleep(0.5)

                        line = ser.readline().decode().strip()
                        
                        if line.startswith("OK"):
                            UARTLines.append(line)
                        elif not line.startswith("errlog"):
                            break

                    for line in UARTLines:
                        relevant_number = line.split()[2]
                        if relevant_number in error_codes:
                            error_code = error_codes[relevant_number]
                            if relevant_number == "FFFFFFFF":
                                no_error = True
                            else:
                                errors = True
                                self.text_ctrl.AppendText(f"Error Code: {relevant_number}, Description: {error_code} \n\n")

                        else:
                            self.text_ctrl.AppendText(f"Error Code: {relevant_number}, Not found. Please report your findings. \n")

                    if not errors and no_error:
                        self.text_ctrl.AppendText("Good news! No errors have been found!\n")
                    else:
                        dialog = wx.MessageDialog(None, "Do you want to save the error codes to a text file?", "Save Error Codes", wx.YES_NO | wx.ICON_QUESTION)
                        response = dialog.ShowModal()
                        dialog.Destroy()

                        if response == wx.ID_YES:
                            file_path = save_file_dialog(self)
                            if file_path:
                                with open(file_path, "a") as file:
                                    for line in UARTLines:
                                        relevant_number = line.split()[2]
                                        if relevant_number in error_codes:
                                            error_code = error_codes[relevant_number]
                                            if error_code != "No Errors":
                                                file.write(f"Error Code: {relevant_number}, Description: {error_code} \n \n")
                                self.text_ctrl.AppendText("Error codes saved to error_codes.txt\n")
        except Exception as ex:
            wx.MessageBox(f"An error occurred while connecting to the selected device.\nError details:\n{ex}", "Error", wx.OK | wx.ICON_ERROR)

    def clear_error_codes(self, selected_port):
        try:
            with serial.Serial(selected_port) as ser:
                self.text_ctrl.Clear()
                ser.baudrate = 115200
                ser.rts = True
                ser.timeout = 5.0
                self.text_ctrl.AppendText(f"Selected port: {selected_port}\n\nClearing error logs...\n")
                command = f"errlog clear"
                checksum = self.calculate_checksum(command)
                ser.write((checksum + "\n").encode())
                
                time.sleep(0.5)
                line = ser.readline().decode().strip()
                self.text_ctrl.AppendText("Error logs cleared\n")
                self.text_ctrl.AppendText("\n")
                ser.close()
        except Exception as ex:
            wx.MessageBox(f"An error occurred while connecting to the selected device.\nError details:\n{ex}", "Error", wx.OK | wx.ICON_ERROR)

    def submit_error_codes(self, selected_port):
        webbrowser.open(tcuk_url)

    def open_console_repair_wiki(self):
        webbrowser.open(console_repair_wiki_url)

    def calculate_checksum(self, input_str):
        checksum = sum(ord(char) for char in input_str)
        return f"{input_str}:{checksum & 0xFF:02X}"

    def parse_error_codes(self, xml_file):
        error_codes = {}
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for errorCode in root.findall('errorCode'):
            code = errorCode.find('ErrorCode').text.strip()
            description = errorCode.find('Description').text.strip()
            error_codes[code] = description
        return error_codes

    def custom_command(self, port_name):
        dialog = wx.TextEntryDialog(None, "Enter custom command:", "Custom Command")
        if dialog.ShowModal() == wx.ID_OK:
            command = dialog.GetValue()
            dialog.Destroy()
            if command:
                self.text_ctrl.AppendText(f"Sending custom command: {command}\n")
                try:
                    with serial.Serial(port_name) as ser:
                        ser.baudrate = 115200
                        ser.rts = True
                        ser.timeout = 5.0
                        
                        # Send the command twice
                        checksum = self.calculate_checksum(command)
                        ser.write((checksum + "\n").encode())
                        
                        time.sleep(0.5)
                        ser.readline().decode().strip()  # Discard the first response
                        
                        ser.write((checksum + "\n").encode())
                        
                        time.sleep(0.5)
                        response = ser.readline().decode().strip()
                        self.text_ctrl.AppendText(f"Response: {response}\n")
                except Exception as ex:
                    wx.MessageBox(f"An error occurred while sending the custom command.\nError details:\n{ex}", "Error", wx.OK | wx.ICON_ERROR)
            else:
                self.text_ctrl.AppendText("No command entered.\n")
        else:
            dialog.Destroy()

class BIOSModifierPanel(wx.Panel):
    def __init__(self, parent):
        super(BIOSModifierPanel, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='BIN File:')
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.filePicker = wx.FilePickerCtrl(self, message="Choose a file", wildcard="PS5 BIN Files (*.bin)|*.bin")
        hbox1.Add(self.filePicker, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='PS5 Model:')
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        self.ps5ModelText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox2.Add(self.ps5ModelText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='Serial Number:')
        hbox3.Add(st3, flag=wx.RIGHT, border=8)
        self.boardSerialText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox3.Add(self.boardSerialText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='Motherboard Serial:')
        hbox4.Add(st4, flag=wx.RIGHT, border=8)
        self.moboSerialText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox4.Add(self.moboSerialText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='WiFi MAC Address:')
        hbox5.Add(st5, flag=wx.RIGHT, border=8)
        self.wifiMacText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox5.Add(self.wifiMacText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        st6 = wx.StaticText(self, label='LAN MAC Address:')
        hbox6.Add(st6, flag=wx.RIGHT, border=8)
        self.lanMacText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox6.Add(self.lanMacText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox6, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        st7 = wx.StaticText(self, label='Board Variant:')
        hbox7.Add(st7, flag=wx.RIGHT, border=8)
        self.boardVariantText = wx.TextCtrl(self, style=wx.TE_READONLY)
        hbox7.Add(self.boardVariantText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox7, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hboxseperator = wx.BoxSizer(wx.HORIZONTAL)
        hboxseperator.AddStretchSpacer()
        stseperator = wx.StaticText(self, label='---------------------------------------- Create New BIOS ----------------------------------------', style=wx.ALIGN_CENTER)
        hboxseperator.Add(stseperator, flag=wx.RIGHT, border=8)
        hboxseperator.AddStretchSpacer()
        vbox.Add(hboxseperator, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hboxtext = wx.BoxSizer(wx.HORIZONTAL)
        hboxtext.AddStretchSpacer()
        sttext = wx.StaticText(self, label='Use your old bios and change the details below to create and save a new bios.')
        hboxtext.Add(sttext, flag=wx.RIGHT, border=8)
        hboxtext.AddStretchSpacer()
        vbox.Add(hboxtext, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox9 = wx.BoxSizer(wx.HORIZONTAL)
        st9 = wx.StaticText(self, label='New PS5 Model Type:')
        hbox9.Add(st9, flag=wx.RIGHT, border=8)
        self.ps5EditionChoice = wx.Choice(self, choices=["", "Disc Edition", "Digital Edition"])
        hbox9.Add(self.ps5EditionChoice, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox9, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        st8 = wx.StaticText(self, label='New Serial Number:')
        hbox8.Add(st8, flag=wx.RIGHT, border=8)
        self.newBoardSerialText = wx.TextCtrl(self)
        hbox8.Add(self.newBoardSerialText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox8, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox12 = wx.BoxSizer(wx.HORIZONTAL)
        st12 = wx.StaticText(self, label='New Motherboard Serial:')
        hbox12.Add(st12, flag=wx.RIGHT, border=8)
        self.newMoboSerialText = wx.TextCtrl(self)
        hbox12.Add(self.newMoboSerialText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox12, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox10 = wx.BoxSizer(wx.HORIZONTAL)
        st10 = wx.StaticText(self, label='New WiFi MAC Address:')
        hbox10.Add(st10,flag=wx.RIGHT, border=8)
        self.newWifiMacText = wx.TextCtrl(self)
        hbox10.Add(self.newWifiMacText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox10, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox11 = wx.BoxSizer(wx.HORIZONTAL)
        st11 = wx.StaticText(self, label='New LAN MAC Address:')
        hbox11.Add(st11, flag=wx.RIGHT, border=8)
        self.newLanMacText = wx.TextCtrl(self)
        hbox11.Add(self.newLanMacText, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox11, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox13 = wx.BoxSizer(wx.HORIZONTAL)
        st13 = wx.StaticText(self, label='New Board Variant:')
        hbox13.Add(st13, flag=wx.RIGHT, border=8)
        self.newBoardVariantChoice = wx.Choice(self, choices=[
            "", "CFI-1000A", "CFI-1000B", "CFI-1002A", "CFI-1008A",
            "CFI-1014A", "CFI-1015A", "CFI-1015B", "CFI-1016A", "CFI-1018A",
            "CFI-1102A", "CFI-1108A", "CFI-1109A", "CFI-1114A",
            "CFI-1115A", "CFI-1116A", "CFI-1118A", "CFI-1208A", "CFI-1215A",
            "CFI-1216A",
        ])
        hbox13.Add(self.newBoardVariantChoice, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox13, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox14 = wx.BoxSizer(wx.HORIZONTAL)
        download_button = wx.Button(self, label="Download Fresh BIOS")
        download_button.Bind(wx.EVT_BUTTON, self.download_bios)
        hbox14.Add(download_button, flag=wx.ALL | wx.CENTER, border=10)
        btn1 = wx.Button(self, label='Save New Bios')
        btn1.Bind(wx.EVT_BUTTON, self.OnSave)
        hbox14.Add(btn1, flag=wx.ALL | wx.CENTER, border=10)
        vbox.Add(hbox14, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, border=10)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnFilePicked, self.filePicker)


    def OnFilePicked(self, event):
        filename = self.filePicker.GetPath()
        with open(filename, 'rb') as f:
            self.data = f.read()

        self.ps5ModelText.SetValue(self.extract_model_info(self.data))
        self.moboSerialText.SetValue(self.extract_mobo_serial(self.data))
        self.boardSerialText.SetValue(self.extract_board_serial(self.data))
        self.wifiMacText.SetValue(self.extract_wifi_mac(self.data))
        self.lanMacText.SetValue(self.extract_lan_mac(self.data))
        self.boardVariantText.SetValue(self.extract_board_variant(self.data))

    def OnSave(self, event):
        new_board_serial = self.newBoardSerialText.GetValue().encode('utf-8')

        if len(new_board_serial) > 10:
            wx.MessageBox("New board serial must be 10 bytes or less.", "Error", wx.ICON_ERROR)
            return

        edition_choice = self.ps5EditionChoice.GetStringSelection()

        new_data = bytearray(self.data)
        board_offset = 0x1C7210

        if new_board_serial:
            new_data[board_offset:board_offset+len(new_board_serial)] = new_board_serial

        if edition_choice == "Digital Edition":
            offset = self.data.find(b'\x22\x02\x01\x01')
            if offset != -1:
                new_data[offset+1] = 0x03
        elif edition_choice == "Disc Edition":
            offset = self.data.find(b'\x22\x03\x01\x01')
            if offset != -1:
                new_data[offset+1] = 0x02

        new_wifi_mac = self.newWifiMacText.GetValue().replace(':', '')
        new_lan_mac = self.newLanMacText.GetValue().replace(':', '')

        if len(new_wifi_mac) == 12:
            new_data[0x1C73C0:0x1C73C0 + 6] = bytearray.fromhex(new_wifi_mac)

        if len(new_lan_mac) == 12:
            new_data[0x1C4020:0x1C4020 + 6] = bytearray.fromhex(new_lan_mac)

        new_mobo_serial = self.newMoboSerialText.GetValue().encode('utf-8')
        if new_mobo_serial:
            new_data[0x1C7200:0x1C7200 + len(new_mobo_serial)] = new_mobo_serial

        new_board_variant = self.newBoardVariantChoice.GetStringSelection()
        if new_board_variant:
            new_variant_bytes = new_board_variant.encode('utf-8')
            new_data[0x1C7230:0x1C7230 + len(new_variant_bytes)] = new_variant_bytes

        save_dialog = wx.FileDialog(self, "Save modified BIN file", wildcard="PS5 BIN Files (*.bin)|*.bin", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save_dialog.ShowModal() == wx.ID_CANCEL:
            return
        new_filename = save_dialog.GetPath()
        with open(new_filename, 'wb') as f:
            f.write(new_data)
            wx.MessageBox("BIN file saved successfully.", "Success", wx.ICON_INFORMATION)
        self.filePicker.SetPath(new_filename)
        self.OnFilePicked(event)
        save_dialog.Destroy()

    def extract_model_info(self, data):
        offset_one = data.find(b'\x22\x02\x01\x01')
        offset_two = data.find(b'\x22\x03\x01\x01')

        if offset_one != -1:
            return "Disc Edition"
        elif offset_two != -1:
            return "Digital Edition"
        else:
            return "Unknown"

    def extract_mobo_serial(self, data):
        return self.decode_bytes(data, 0x1C7200, 16)

    def extract_board_serial(self, data):
        return self.decode_bytes(data, 0x1C7210, 10)

    def extract_wifi_mac(self, data):
        return ':'.join(f'{b:02X}' for b in data[0x1C73C0:0x1C73C0 + 6])

    def extract_lan_mac(self, data):
        return ':'.join(f'{b:02X}' for b in data[0x1C4020:0x1C4020 + 6])

    def extract_board_variant(self, data):
        board_variant = self.decode_bytes(data, 0x1c7226, 19)

        cleaned_board_variant = board_variant.replace("FF", "").replace("-", "").strip()

        try:
            decoded_variant = bytes.fromhex(cleaned_board_variant).decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            decoded_variant = "Invalid Variant"

        region = "Unknown Region"

        if decoded_variant.endswith(("00A", "00B")):
            region = "Japan"
        elif decoded_variant.endswith(("01A", "01B", "15A", "15B")):
            region = "US / Canada / North America"
        elif decoded_variant.endswith(("02A", "02B")):
            region = "Australia / New Zealand / Oceania"
        elif decoded_variant.endswith(("03A", "03B")):
            region = "United Kingdom / Ireland"
        elif decoded_variant.endswith(("04A", "04B")):
            region = "Europe / Middle East / Africa"
        elif decoded_variant.endswith(("05A", "05B")):
            region = "South Korea"
        elif decoded_variant.endswith(("06A", "06B")):
            region = "Southeast Asia / Hong Kong"
        elif decoded_variant.endswith(("07A", "07B")):
            region = "Taiwan"
        elif decoded_variant.endswith(("08A", "08B")):
            region = "Russia / Ukraine / India / Central Asia"
        elif decoded_variant.endswith(("09A", "09B")):
            region = "Mainland China"
        elif decoded_variant.endswith(("11A", "11B", "14A", "14B")):
            region = "Mexico / Central America / South America"
        elif decoded_variant.endswith(("16A", "16B")):
            region = "Europe / Middle East / Africa"
        elif decoded_variant.endswith(("18A", "18B")):
            region = "Singapore / Korea / Asia"

        return f"{decoded_variant} - {region}"

    def decode_bytes(self, data, offset, length):
        try:
            return data[offset:offset + length].decode("utf-8")
        except UnicodeDecodeError:
            return binascii.hexlify(data[offset:offset + length]).decode("utf-8")

    def download_bios(self, event):
        webbrowser.open(download)



class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        uart_tool_panel = UARTToolFrame(notebook)
        bios_modifier_panel = BIOSModifierPanel(notebook)


        notebook.AddPage(uart_tool_panel, "UART Tool")
        notebook.AddPage(bios_modifier_panel, "BIOS Modifier")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

if __name__ == '__main__':
    download_error_codes_xml(url, filename)
    app = wx.App()
    MainFrame(None, title='PS5 Toolbox v0.2')
    app.MainLoop()
    wx.Exit()
