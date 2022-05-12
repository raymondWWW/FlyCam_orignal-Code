"""
Test code for having two windows:
1) Video Stream
2) Normal GUI (here, just a button)

Questions:
-Do I need another thread?
-How do I get PiRGBArray to run inside of a while loop? Can you progress with an iterator using a while loop?
-Is OpenCV window with webcam faster than PySimpleGUI?


"""

import PySimpleGUI as sg


def main():
    print("Main")

    # Setup two layouts, one for video, the other for a button
    # layout_video = [[sg.Image(filename='', key='-IMAGE-')]]

    # Setup two windows: video and button

    # While loop for GUI

    pass


if __name__ == "__main__":
    main()
