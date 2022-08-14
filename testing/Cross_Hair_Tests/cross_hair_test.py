"""
Cross Hair Test

Algorithm:
GUI, button to Update Image (takes from preview)
GUI, same circle radius as SimpleGUI
Get preview dimensions
Load image
Make a copy of image
Get dimensions of image
Get center x, center y.
On Copy, Draw line, center x, from min y to max y
On Copy, Draw line, center y, from min x to max x
On copy, Draw circle at center x/y with radius
Display Image


TODO:
-Circle overlay opacity? Color change?
-Research ellipse?
"""
import PySimpleGUI as sg

# Events
LOAD_IMAGE = "Update/Load Image"

# Circle Mask
CIRCLE_XC = 1350
CIRCLE_YC = 960
CIRCLE_CENTER = (CIRCLE_XC, CIRCLE_YC)
CIRCLE_RADIUS = 760
CIRCLE_COLOR = (0, 0, 255)
CIRCLE_THICKNESS = 3

RAD_KEY = "-RADIUS-"
RAD_MINUS_TEN = "-RAD MINUS_TEN-"
RAD_MINUS_ONE = "-RAD MINUS_ONE-"
RAD_PLUS_ONE = "-RAD PLUS ONE-"
RAD_PLUS_TEN = "-RAD PLUS TEN-"


def update_circle(event, values, window):
    global CIRCLE_XC, CIRCLE_YC, CIRCLE_RADIUS, CIRCLE_CENTER

    if event == LOAD_IMAGE:
        CIRCLE_RADIUS = int(values[RAD_KEY])

    if event == RAD_MINUS_TEN:
        CIRCLE_RADIUS -= 10
    elif event == RAD_MINUS_ONE:
        CIRCLE_RADIUS -= 1
    elif event == RAD_PLUS_ONE:
        CIRCLE_RADIUS += 1
    elif event == RAD_PLUS_TEN:
        CIRCLE_RADIUS += 10

    CIRCLE_CENTER = (CIRCLE_XC, CIRCLE_YC)
    window[RAD_KEY].update(CIRCLE_RADIUS)


def main():
    print("Main")

    # Dummy Image as placecholder
    # folder: D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-25-2022\Code_Pictures_2022-07-25_171105_auto
    # filename: well1_2022-07-25_171110.jpg
    # image_location
    # Dummy resize to 640, 480

    circle_event_list = [RAD_MINUS_TEN, RAD_MINUS_ONE, RAD_PLUS_ONE, RAD_PLUS_TEN]

    # Setup sg theme
    sg.theme("LightGreen")

    # Setup layout
    # Button: Load Image
    # Radius Change, similar to SimpleGUI version.
    layout = [[sg.Button(LOAD_IMAGE)],
              [sg.Text("Circle Radius:"),
               sg.Button("-10", key=RAD_MINUS_TEN), sg.Button("-1", key=RAD_MINUS_ONE),
               sg.Input(CIRCLE_RADIUS, size=(4, 1), key=RAD_KEY),
               sg.Button("+1", key=RAD_PLUS_ONE), sg.Button("+10", key=RAD_PLUS_TEN)]]

    # Setup window
    window = sg.Window("Cross Hair Test", layout=layout)

    # Start while loop for GUI
    while True:
        event, values = window.read()

        if event in circle_event_list:
            # print("Circle event detected")
            update_circle(event, values, window)

        if event == sg.WIN_CLOSED:
            break
        elif event == LOAD_IMAGE:
            # print(f"Pressed: {LOAD_IMAGE}")
            update_circle(event, values, window)



    print("Closing GUI...")
    pass


if __name__ == "__main__":
    main()


