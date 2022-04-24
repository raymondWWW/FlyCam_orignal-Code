"""
Test Code for Thread Pause and Restart, to fix restart bug for RoboCam

Idea:
-Replicate bug in RoboCam
-Possible solution: have thread in a forever while loop,
 pause thread, then restart upon call. Use global true/false to check if should restart while loop

Code Sources:
https://stackoverflow.com/questions/33640283/thread-that-i-can-pause-and-resume

"""

import PySimpleGUI as sg


# Define thread function

#  Load up a list

#  run for loop going through list


def main():
    print("Main")

    # Setup 2 button layout, start/stop
    layout = [[sg.Button("Start", size=(10, 1)), sg.Button("Stop", size=(10, 1))]]

    # Setup window
    window = sg.Window("Thread Test", layout, location=(100, 100))

    # Start While Loop

    #  If/Else
    #  Close button
    #  Start
    #   Run thread
    #  Stop
    #   Pause thread



    pass


if __name__ == "__main__":
    main()
