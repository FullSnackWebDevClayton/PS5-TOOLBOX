import wx
import serial.tools.list_ports
import serial
import time
import os
import xml.etree.ElementTree as ET
import datetime
import requests
import webbrowser

current_date_time = datetime.datetime.now()
formatted_date_time = current_date_time.strftime("%d-%m-%Y %H:%M:%S")
url = "http://198.244.234.174:8001/generate-xml"
tcuk_url = "http://www.consolerepair.wiki/en/submit-uart-code"
donate_url = "https://buymeacoffee.com/techcentreuk"
console_repair_wiki_url = "http://www.consolerepair.wiki"
filename = "error_codes.xml"

def appsupportdir():
    if os.name == 'nt':  # Windows
        appdata = os.getenv('APPDATA')
        return os.path.expandvars(appdata)
    elif os.name == 'posix':  # macOS/Linux
        home = os.path.expanduser('~')
        return os.path.join(home, 'Library', 'Application Support')
    else:
        # Handle other operating systems if needed
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
    except Exception as e:
        print("An error occurred while downloading the newest database:", e)

def save_file_dialog(parent_frame):
    wildcard = "Text files (*.txt)|*.txt"
    dialog = wx.FileDialog(parent_frame, message="Save file", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dialog.ShowModal() == wx.ID_CANCEL:
        return None
    return dialog.GetPath()

class UARTToolFrame(wx.Frame):
    def __init__(self):
        super(UARTToolFrame, self).__init__(None, title="PS5 UART Tools - By Tech Centre UK", size=(800, 600))
        self.panel = wx.Panel(self)
        
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

if __name__ == "__main__":
    download_error_codes_xml(url, filename)
    app = wx.App(False)
    frame = UARTToolFrame()
    app.MainLoop()
    wx.Exit()
