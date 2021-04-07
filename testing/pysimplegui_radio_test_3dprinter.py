# PySimpleGUI Radio Testing with 3D Printer Relative Movements
# Without actually using a 3D Printer, only display numbers

# Import Library


# Create constants for:
# Radio Keys
# X+, X-, Y+, Y-, Z+, or Z-
# WINDOW_GUI_TIMEOUT

# User Defined Functions

# Define function, run_relative(direction, values)
#   Converts input into GCODE String, then calls run_gcode from printer module (not implemented in this demo)
#   Inputs: takes string direction (X+, X-, Y+, Y-, Z+, or Z-)
#           values from window.read()
#   Initialize relative_coordinates variable to direction and 0.00 (example: X0.00, no movements)
#   Initialize move_amount to 0.00
#   Use if/elif chain to check which radio button is true (0.1, 1, or 10)
        # If values[-REL_TENTH-] == True
            # Example If 0.1 true, change relative coordinates to X-0.10
        # else if the values of relative one is True
            # Make movement amount into 1.00
        # else if the values of relative ten is True
            # Make movement amount into 1.00
#   Use string formatting to create GCode string (example: G0X-1.00)
#   TODO: Test if X+ works with GCODE
#   TODO: Extruder Speed Adjustment

# Create Layout
# Example:  [] 0.1 mm  [] 1 mm  [] 10 mm
#                       [Up Button]
#               [LEFT]               [Right]
#                         [Down]
#     Keys:    -REL_TENTH-, -REL_ONE-, -REL_TEN-

# Set Window


# Use While Loop to Execute GUI
    # get event and values from window.read()
    # Have event to close window

    # Only events/values for if Up Button was pressed
    #    If buttons are pressed, pass on direction (X+, X-, Y+, Y-, Z+, or Z-) and values of radio keys

# Close Window