"""
Frequency and Time Library Tests

Purpose: For color sensor accuracy.

Code Sources:
https://www.geeksforgeeks.org/python-time-monotonic-method/
https://www.geeksforgeeks.org/timeit-python-examples/
https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/

"""

import matplotlib.pyplot as plt
import time
import timeit


# Pulse Repetition Frequency
# Fixed Time, variable number of cycles
def prf(time_to_wait):
    # Get number of cycles for a fixed time.
    # Results of internal elapsed time vs external (end - start)
    # Same for Monotonic, I'm curious to see what it's like for the actual test case.
    elapsed_time = 0
    num_cycles = 0

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        # Code to get PWM Falling Goes Here
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()

    # print(f"Expected Time to Wait: {time_to_wait} seconds")
    # print(f"While Loop Execution Time (seconds): {end - start}")
    # print(f"Elapsed Time Inside While Loop (seconds): {elapsed_time}")
    # print(f"Number of Cycles: {num_cycles}")
    return num_cycles


def get_duration(num_cycles):
    start = time.monotonic()
    for i in range(num_cycles):
        # Get Color Sensor Data Here
        continue
    end = time.monotonic()
    duration = end - start # In seconds
    return duration


def main():

    # Tests with monotonic()
    # time.monotonic_ns() seems to round stuff.
    # print("time.monotonic()")
    # for i in range(10):
    #     start = time.monotonic()
    #
    #     time.sleep(1)
    #
    #     end = time.monotonic()
    #
    #     # print(f"Value of the monotonic clock (in fractional seconds): {end}")
    #     print(f"Time elapsed during the process (seconds): {end - start}")
    #
    # print("time.monotonic_ns()")
    # for i in range(10):
    #     start = time.monotonic_ns()
    #
    #     time.sleep(1)
    #
    #     end = time.monotonic_ns()
    #
    #     # print(f"Value of the monotonic clock (in fractional seconds): {end}")
    #     print(f"Time elapsed during the process (nanoseconds): {end - start}")
    pass


def main3():
    time_to_wait = 1 # Seconds
    # num_cycles = prf(time_to_wait)
    # print(f"Freq: {num_cycles / time_to_wait} Hz")

    # print("Running prf()...")
    # num_cycles_list = []
    # for i in range(100):
    #     num_cycles = prf(time_to_wait)
    #     num_cycles_list.append(num_cycles)
    #
    # print("Done Running PRF Code, making boxplot")
    # # print(num_cycles_list)
    #
    # fig = plt.figure()
    #
    # plt.boxplot(num_cycles_list)
    #
    # plt.show()

    print("Running get_duration(num_cycles)...")
    num_cycles = 10
    duration_list = []
    for i in range(10):
        duration = get_duration(num_cycles)
        duration_list.append(duration)

    print("Done Running get_duration Code, making boxplot")
    # print(num_cycles_list)

    fig = plt.figure()

    plt.boxplot(duration_list)

    plt.show()

    pass


if __name__ == "__main__":
    # main()
    # main2()
    main3()
    # linear_time()
    pass
