"""
Test code for having two windows:
1) Video Stream
2) Normal GUI (here, just a button)

Questions:
-Do I need another thread?
  -Not Necessarily, if using OpenCV
-How do I get PiRGBArray to run inside of a while loop? Can you progress with an iterator using a while loop?
-Is OpenCV window with webcam faster than PySimpleGUI?
   -If there is a different, I can't tell.

Links for Later:
https://python.hotexamples.com/examples/picamera/PiCamera/capture_continuous/python-picamera-capture_continuous-method-examples.html
PiVideoStream Class with Threading

https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.capture_continuous

Try out
https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.start_preview

Ideas: flush GUI image window?
"""

import cv2
import PySimpleGUI as sg
import time

def main():
    print("Main")

    # Setup PySimpleGUI Theme
    sg.theme('LightGreen')

    # Setup two layouts, one for video, the other for a button
    layout_video = [[sg.Image(filename='', key='-IMAGE-')]]
    layout_control = [[sg.Button("A Button")]]

    # Setup two windows: video and button
    window_video = sg.Window("Video", layout_video, location=(0, 0))
    window_control = sg.Window("Button", layout_control, location=(700, 0))

    cap = cv2.VideoCapture(0)

    # While loop for GUI
    counter = 0
    while True:

        # Video Window
        start = time.time()
        event_video, values_video = window_video.read(timeout=0)

        ret, frame = cap.read()

        if event_video == 'Exit' or event_video == sg.WIN_CLOSED:
            break

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window_video['-IMAGE-'].update(data=imgbytes)
        end = time.time()
        print(f"Stream : {end - start}")

        start = time.time()
        cv2.imshow("OpenCV", frame)
        end = time.time()
        print(f"OpenCV : {end - start}")

        # Other Window
        event_control, values_control = window_control.read(timeout=0)
        if event_control == 'Exit' or event_control == sg.WIN_CLOSED:
            break
        elif event_control == "A Button":
            print("You Pushed a Button")



    pass


if __name__ == "__main__":
    main()
