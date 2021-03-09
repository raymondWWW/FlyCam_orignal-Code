"""
Load Settings YAML files for 3dprinter_start_experiment

Purpose: Replaces Common Python file, allows for future GUI usage where the YAML files can be edited and reloaded
"""

# Import libraries, yaml
import yaml
# Create Constants Variables, like in Common file

# Load YAML files, store into constants
# Load YAML Settings

# Placeholder Constants
# Monoprice Maker Select 3D Printer V2, Lab 3D Printer
DEVICE_PATH = '/dev/ttyUSB0'
BAUDRATE = 115200     # 115200: for Marlin Firmware
TIMEOUT_TIME = 1      # Wait 1 second
REBOOT_WAIT_TIME = 5  # 5 seconds

# Load GCODE Strings, or put them here temporarily
# GCode Strings
HOME = "G28"
ABSOLUTE_POS = "G90"
RELATIVE_POS = "G91"

# Which Project? Will influence which settings are loaded
# PROJECT = "mht"
PROJECT = "cell_sensor"

# Load YAML Settings
with open("connection_settings.yaml") as file:
    # The fullloader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    connection_settings_dict = yaml.load(file, Loader=yaml.FullLoader)
    # How to access dict items
    # print(connection_settings_dict["cell_sensor"]["monoprice"]["device_path"])
    DEVICE_PATH = connection_settings_dict[PROJECT]["monoprice"]["device_path"]
    BAUDRATE = connection_settings_dict[PROJECT]["monoprice"]["baudrate"]
    TIMEOUT_TIME = connection_settings_dict[PROJECT]["monoprice"]["timeout_time"]
    REBOOT_WAIT_TIME = connection_settings_dict[PROJECT]["monoprice"]["reboot_wait_time"]

# User Defined function that can change Constants by having user load up a YAML file and choosing a different 3D printer
# TODO: Later feature
# TODO: Research project structure for GUI and Settings file

