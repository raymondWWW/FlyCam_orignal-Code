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
-Check if default number, does it change later?
-Color Wheel,
"""
import cv2
import PySimpleGUI as sg

from os.path import join

# Events
LOAD_IMAGE = "Update/Load Image"

# Circle Mask
CIRCLE_RADIUS = 100
CIRCLE_COLOR = (0, 0, 255) # BGR
CIRCLE_THICKNESS = 1

CIRCLE_THICKNESS_KEY = "-=CIRCLE THICKNESS KEY=-"

RAD_KEY = "-RADIUS-"
RAD_MINUS_TEN = "-RAD MINUS_TEN-"
RAD_MINUS_ONE = "-RAD MINUS_ONE-"
RAD_PLUS_ONE = "-RAD PLUS ONE-"
RAD_PLUS_TEN = "-RAD PLUS TEN-"

LINE_THICKNESS_KEY = "-=LINE THICKNESS KEY=-"
LINE_THICKNESS = 1


def update_circle(event, values, window):
    global CIRCLE_RADIUS, CIRCLE_THICKNESS

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

    # Update Circle Thickness
    circle_thick_number = int(values[CIRCLE_THICKNESS_KEY])
    CIRCLE_THICKNESS = circle_thick_number

    # Update Window Values for Circle Radius
    window[RAD_KEY].update(CIRCLE_RADIUS)

    # Update Line Thickness
    update_line_thickness(values)

    # Draw/Update the Image
    draw_on_image()


def update_line_thickness(values):
    global LINE_THICKNESS

    # Update LINE_THICKNESS global variable
    thick_number = int(values[LINE_THICKNESS_KEY])
    LINE_THICKNESS = thick_number
    pass


def draw_on_image():

    # Temp image get
    image = get_dummy_image()
    image_edit = image.copy()

    # Make a copy of image
    # Get dimensions of image
    # print(image.shape)
    height, width, ch = image.shape
    # Get center x, center y.
    center_x = int(width / 2)
    center_y = int(height / 2)
    print(f"Center: {center_x, center_y}")

    # On Copy, Draw line, center y, from min x to max x
    # horizontal line
    start_point = (0, center_y)
    end_point = (width, center_y)
    color = (0, 0, 255) # BGR
    image_edit = cv2.line(image_edit, start_point, end_point, color, LINE_THICKNESS)

    # On Copy, Draw line, center x, from min y to max y
    # vertical line
    start_point = (center_x, 0)
    end_point = (center_x, height)
    image_edit = cv2.line(image_edit, start_point, end_point, color, LINE_THICKNESS)

    # On copy, Draw circle at center x/y with radius
    center_coordinates = (center_x, center_y)
    image_edit = cv2.circle(image_edit, center_coordinates, CIRCLE_RADIUS, color, CIRCLE_THICKNESS)

    # Display Image
    cv2.imshow("image_edit", image_edit)
    pass


def get_dummy_image():
    # Dummy Image as placecholder
    # folder: D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-25-2022\Code_Pictures_2022-07-25_171105_auto
    image_folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-25-2022\Code_Pictures_2022-07-25_171105_auto'
    # filename: well1_2022-07-25_171110.jpg
    image_file = r'well1_2022-07-25_171110.jpg'
    # image_location
    image_path = join(image_folder, image_file)
    # Dummy resize to 640, 480
    image = cv2.imread(image_path)
    image_resize = cv2.resize(image, (640, 480))

    return image_resize


def main():
    print("Main")
    # global THICKNESS

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
               sg.Button("+1", key=RAD_PLUS_ONE), sg.Button("+10", key=RAD_PLUS_TEN)],
              [sg.Text("Circle Thickness:"), sg.Input(CIRCLE_THICKNESS, size=(4, 1), key=CIRCLE_THICKNESS_KEY)],
              [sg.Text("Line Thickness:"), sg.Input(LINE_THICKNESS, size=(4, 1), key=LINE_THICKNESS_KEY)],
              [sg.ColorChooserButton("Pick a Color", key="-= COLOR CHOOSER KEY =-")],
              [sg.Button("Show Color", key="Show Color")]]

    # Setup window
    window = sg.Window("Cross Hair Test", layout=layout)

    # Start while loop for GUI
    while True:
        event, values = window.read()

        print(event, values)

        if event in circle_event_list:
            # print("Circle event detected")
            update_circle(event, values, window)


        if event == sg.WIN_CLOSED:
            break
        elif event == LOAD_IMAGE:
            # print(f"Pressed: {LOAD_IMAGE}")

            # Update Line Thickness
            update_line_thickness(values)

            update_circle(event, values, window)

            # draw_on_image()
        elif event == "Show Color":
            print("Color Chosen?")
            # print(values["-= COLOR CHOOSER KEY =-"])


    print("Closing GUI...")
    pass


if __name__ == "__main__":
    main()


