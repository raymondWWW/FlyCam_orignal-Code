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
import time
import threading


# CONSTANTS
START = "Start"
STOP = "Stop"

OPEN_CSV_FILEBROWSE_KEY = "-CSV_INPUT-"

IS_RUNNING_EXPERIMENT = False


def get_list():
    result = [1, 2, 3, 4, 5]
    return result


# Define thread function
def run_experiment(csv_file_path):
    print("Run Experiment")
    print(f"CSV File Path: {csv_file_path}")
    #  Load up a list
    num_list = get_list()
    len_num_list = len(num_list)

    counter = 1
    while True:
        print(f"Starting While Loop Counter: {counter}")
        time.sleep(1)

        for item in num_list:
            print(f"item: {item}")

        if not IS_RUNNING_EXPERIMENT:
            print("Not running experiment, stopping function")
            return

        counter += 1

    # print("Done Running Run Experiment")

    pass


def main():
    print("Main")

    global IS_RUNNING_EXPERIMENT

    # Setup 2 button layout, start/stop
    layout = [ [sg.Input(), sg.FileBrowse(key=OPEN_CSV_FILEBROWSE_KEY)],
               [sg.Button(START, size=(10, 1)), sg.Button(STOP, size=(10, 1))] ]

    # Setup window
    window = sg.Window("Thread Test", layout, location=(100, 100))

    # Threading Setup
    # Initialize empty experiment_thread object, will be used with "Start Experiment" is pushed
    experiment_thread = threading.Thread()

    # Initialize threading event (Allows you to stop the thread)
    thread_event = threading.Event()

    # Start While Loop
    while True:

        event, values = window.read(timeout=1)

        if event == sg.WIN_CLOSED:
            break
        elif event == START:
            print(f"You pressed: {START}")
            IS_RUNNING_EXPERIMENT = True

            csv_file_path = values[OPEN_CSV_FILEBROWSE_KEY]

            experiment_thread = threading.Thread(target=run_experiment, args=(csv_file_path,), daemon=True)
            experiment_thread.start()
            # run_experiment()
        elif event == STOP:
            IS_RUNNING_EXPERIMENT = False
            print(f"You pressed: {STOP}")

    #  If/Else
    #  Close button
    #  Start
    #   Run thread
    #  Stop
    #   Pause thread

    print("GUI Closed")

    pass


if __name__ == "__main__":
    main()
