"""
3D Printer Sampler

Purpose: Opens up path list YAML file,
         goes to each location in path list,
         converts int values to Gcode string,
         then takes picture/records/previews.
"""

# import libraries
# camera, serial, time, yaml

# Import module that loads up 3D Printer settings and such
# Note: Bring over YAML files for 3D Printer Settings, and Path List

# Setup camera and printer

# User Defined Functions

# Define initial_setup() function for 3D printer

# Define function, run_gcode_ that runs a GCode string

# define function go_home() to go to home coordinates

# Define function to open YAML paths file, then extracts/returns paths list

# Define function, start_experiment with flag isPreviewModeOn, isRecordingModeOn
#   If isPreviewModeOn is true, no pictures/video taken, but camera stays on to show location movements
#   else take picture or video (check isRecordingModeOn flag)

# Define function, main, to run things