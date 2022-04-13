"""
Test for GUI to bugfix restart bug.

Algo:

"Streaming" GUI,
click start button, pause "streaming",

New GUI with "stop" and loop continues. Stop button will stop function


"""

import PySimpleGUI as sg
import time

def run_exp_gui():
    # Experiment GUI, have a stop button, runs experiment loop
    print("Running Experiment GUI")

    # Should reload CSV file for locations

    loc_list = ["a", "b", "c", "d", "e", "f"]
    loc_list_len = len(loc_list)
    sg.theme('Light Brown 3')

    layout_exp = [[sg.Button('Stop Experiment', size=(20, 40))]]

    window_exp = sg.Window('Main GUI Window', layout_exp, finalize=True)

    # timeout = thread = None
    timeout = 1000 # In millisec

    index = 0
    counter = 0
    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window_exp.read(timeout=timeout)

        # Run Experiment
        print(f"Index: {index}")
        print(loc_list[index])

        if index == loc_list_len - 1:
            index = 0
        else:
            index += 1


        if event.startswith('Stop'):
            print("You Pressed Stop")
            break

    window_exp.close()

    pass


def run_main_gui():
    # Setup GUI, have a single start button

    sg.theme('Light Brown 3')

    layout = [[sg.Button('Start Experiment', size=(20, 20))]]

    window = sg.Window('Main GUI Window', layout, finalize=True)

    timeout = thread = None
    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read(timeout=timeout)
        # print(event, values)

        if event.startswith('Start'):
            print("You Pressed Start")
            run_exp_gui()

    pass


def main():
    print("main")
    run_main_gui()
    pass


if __name__ == "__main__":
    main()
