"""
Simulate Color Sensor RGBC Data to do data analysis.

-Save PRF and non-PRF data to CSV.
-Create box plots

Tests:

Q1: Increase precision of non-PRF by increasing fixed number of cycles?

Q2: Decrease speed of PRF while maintaining precision by decreasing fixed time to wait?

Q2A: For both PRF and non-PRF best case scenario, do they have similar precision?
-What is similar precision? Small Variation? Similar Variation with box plot?

Q3: When switching to manual control of scaled output frequency, will 100% match previous setup?

Q4: How does precision change with 20% output? 2%? 100% is supposed to be the least accurate. Run same tests as Q1 and Q2.


Q1, data to collect:
- Number of cycles for RGBC, fixed. Cycles: 10, 100, 1000, 10k, 20k, 30k
- Elapsed time for RBC, same fixed cycles.
- Calculated: Frequency for RGBC: fixed cycles / elapsed time

Q2, data to collect:
- Number of cycles for RGB, not fixed.
- For fixed time to wait: 2s, 1s, 0.75s, 0.5s, 0.25s, 0.1s.
- External and Internal Time too, mark on box plot where fixed time is. Expected vs actual.
- Calculated: Frequency for RGBC:
   - num of cycles / external
   - num of cycles / internal
   - num of cycles / expected time to wait.

Q2A, after finding best case scenario for both separately, run both at the same time.

Plots:
Q1:
- RGBC are 4 columns, each column has elapsed time for each of the fixed number of cycles (if there is room)
   - Else, they all get their own figure.
- RGBC are 4 column, each color shows calculated frequency for each of the number of cycles.
*Note: Look for best case scenario to compare with PRF

Q2:
- RGBC are 4 columns, each column has external vs internal time with expected time shown as horizontal line.
   Each row is the fixed time to wait, so 5 rows. If no room, separate figure.
- RGBC are 4 columns, each column has calculated frequency for all 6 of the fixed times to wait.
* Note: Look for best case scenario to compare with non-PRF.

Q3: Repeat Q1 and Q2? Using 100% scaled output frequency. Or just aim for best case scenario.

Q4: Repeat Q1 and Q2 for different scaled outputs: 20% and 2%.


Code Sources:
https://datagy.io/python-pretty-print-dictionary/
https://www.geeksforgeeks.org/how-to-create-dataframe-from-dictionary-in-python-pandas/
"""

import json
import pandas as pd
import random

import RPi.GPIO as GPIO
import time

from os.path import join

# 100% Output Frequency, in Hz
# Format: (min, max)
CLEAR_RANGE = (16000, 24000)
BLUE_RANGE = (11200, 21600)
RED_RANGE = (14000, 24000)
GREEN_RANGE = (8000, 19200)

# TODO: 20%
"""
CLEAR_RANGE_20 = (16000, 24000)
BLUE_RANGE_20 = (11200, 21600)
RED_RANGE_20 = (14000, 24000)
GREEN_RANGE_20 = (8000, 19200)
"""

# TODO: 2%

SAVE_FOLDER = r'/home/pi/Projects/Color Sensor/CSVs'

color_keys = ['red', 'green', 'blue', 'clear']
prf_keys = ["number_of_cycles", "external_time", "internal_time", "freq_ext", "freq_int", "freq_expected"]

non_prf_keys = ["frequency_(Hz)", "time_(s)"]

# Variables to try
# Q1
# fixed_cycles = [10, 100, 1000, 10000, 20000, 30000]
fixed_cycles = [10]

# Q2
# fixed_times = [2.0, 1.0, 0.75, 0.5, 0.25, 0.1]
fixed_times = [1.0]

# Sensor Pins, Broadcom (BCM) Numbering System
# Use the number after GPIO
S2 = 23
S3 = 24
OUT = 25
SIGNAL = OUT

S0 = 16
S1 = 20
# Note: OE is Output Enable
# OE


# Color Sensor Functions

# PRF Functions
def get_red_prf(time_to_wait):
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_green_prf(time_to_wait):
    # GREEN: S2: HIGH, S3: HIGH
    # Set S2 and S3 to HIGH to capture green
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_blue_prf(time_to_wait):
    # BLUE: S2: LOW, S3: HIGH
    # Set S2 to LOW and S3 to HIGH to capture blue
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_clear_prf(time_to_wait):
    # CLEAR: S2: HIGH, S3: LOW
    # Set S2 to HIGH and S3 to LOW to capture clear
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


# Non-PRF Functions

# Non-PRF, fixed cycles, variable time.
def get_red_monotonic(number_of_cycles):
    
    # RED: S2: LOW, S3: LOW
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(number_of_cycles):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    red  = number_of_cycles / duration   #in Hz
    # print(f"RED: {red} Hz")
    return red, duration


def get_green_monotonic(number_of_cycles):
    
    # GREEN: S2: HIGH, S3: HIGH
    # Set S2 and S3 to HIGH to capture green
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(number_of_cycles):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    green  = number_of_cycles / duration   #in Hz
    # print(f"green: {green} Hz")
    return green, duration


def get_blue_monotonic(number_of_cycles):
    
    # BLUE: S2: LOW, S3: HIGH
    # Set S2 to LOW and S3 to HIGH to capture blue
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(number_of_cycles):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    blue  = number_of_cycles / duration   #in Hz
    # print(f"blue: {blue} Hz")
    return blue, duration


def get_clear_monotonic(number_of_cycles):
    
    # CLEAR: S2: HIGH, S3: LOW
    # Set S2 to HIGH and S3 to LOW to capture clear
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(number_of_cycles):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    clear  = number_of_cycles / duration   #in Hz
    # print(f"clear: {clear} Hz")
    return clear, duration


def color_sensor_setup():
    print("Setting up Color Sensor Pins")
    
    # Set GPIO Mode as Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SIGNAL,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(S2,GPIO.OUT)
    GPIO.setup(S3,GPIO.OUT)
    
    # Output Frequency
    GPIO.setup(S0,GPIO.OUT)
    GPIO.setup(S1,GPIO.OUT)
    
    print("\n")


def set_100_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 100% Output:
    GPIO.output(S0,GPIO.HIGH)
    GPIO.output(S1,GPIO.HIGH)


def set_20_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 20% Output:
    GPIO.output(S0,GPIO.HIGH)
    GPIO.output(S1,GPIO.LOW)


def set_2_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 2% Output:
    GPIO.output(S0,GPIO.LOW)
    GPIO.output(S1,GPIO.HIGH)


def set_power_down_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    # Power Down Output Frequency Scaling: S0: Low,  S1: Low
    
    # Setup Power Down Output:
    GPIO.output(S0,GPIO.LOW)
    GPIO.output(S1,GPIO.LOW)


def end_program():
    GPIO.cleanup()




# Data Collection Functions

def gen_prf_data():
    number_of_cycles = random.randint(8000, 24000)
    external_time = random.random()
    internal_time = random.random()
    return number_of_cycles, external_time, internal_time


# Get RGBC PRF, input: time to wait.
# Simulated data creation
def get_rbgc_prf(time_to_wait):
    # print("get_rbgc_prf")

    # Real world:
    # each color would get each value separately: number_of_cycles, external_time, and internal_time

    results = {}
    # Populate dict:
    for color in color_keys:
        results[color] = {}
        for header in prf_keys:
            results[color][header] = []

    # print(json.dumps(results, indent=4))
    
    # Real Version
    for color in color_keys:
        # color_keys = ['red', 'green', 'blue', 'clear']
        print(f"Getting color: {color}")
        if color == 'red':
            number_of_cycles, external_time, internal_time = get_red_prf(time_to_wait)
            pass
        elif color == 'green':
            number_of_cycles, external_time, internal_time = get_green_prf(time_to_wait)
            pass
        elif color == 'blue':
            number_of_cycles, external_time, internal_time = get_blue_prf(time_to_wait)
            pass
        elif color == 'clear':
            number_of_cycles, external_time, internal_time = get_clear_prf(time_to_wait)
            pass
        
        freq_ext = number_of_cycles / external_time
        freq_int = number_of_cycles / internal_time
        freq_expected = number_of_cycles / time_to_wait
        # Get data for each color
        # Calculate freq_ext, freq_int, freq_expected
        results[color][prf_keys[0]] = number_of_cycles
        results[color][prf_keys[1]] = external_time
        results[color][prf_keys[2]] = internal_time
        results[color][prf_keys[3]] = freq_ext
        results[color][prf_keys[4]] = freq_int
        results[color][prf_keys[5]] = freq_expected

    # Simulated Data
    """
    for color in color_keys:
        # prf_keys = ["number_of_cycles", "external_time", "internal_time", "freq_ext", "freq_int", "freq_expected"]
        # print(color)
        # print(gen_prf_data())
        # **** When Doing Real World Version, use if/else statement to get specific colors, like in non-PRF ****
        number_of_cycles, external_time, internal_time = gen_prf_data()
        freq_ext = number_of_cycles / external_time
        freq_int = number_of_cycles / internal_time
        freq_expected = number_of_cycles / time_to_wait
        # Get data for each color
        # Calculate freq_ext, freq_int, freq_expected
        results[color][prf_keys[0]] = number_of_cycles
        results[color][prf_keys[1]] = external_time
        results[color][prf_keys[2]] = internal_time
        results[color][prf_keys[3]] = freq_ext
        results[color][prf_keys[4]] = freq_int
        results[color][prf_keys[5]] = freq_expected

    """
    # print(json.dumps(results, indent=4))
    # Simulated data:
    # random cycles, ext_time, int_time
    # Calculated freq_ext, freq_int, freq_expected

    # End result, dictionary of dictionary.
    # First layer, keys are colors. Second layer, keys are the data above
    return results


# Get RGBC non-PRF, input: number of cycles
# Simulated data creation
def get_rgbc_non_prf(number_of_cycles):
    print("get_rgbc_non_prf")

    # Real World: Would get each value separately.
    FREQ_HEADER = non_prf_keys[0]
    TIME_HEADER = non_prf_keys[1]

    # color_keys = ['red', 'green', 'blue', 'clear']
    RED_HEADER = color_keys[0]
    GRN_HEADER = color_keys[1]
    BLU_HEADER = color_keys[2]
    CLR_HEADER = color_keys[3]

    # Simulated:
    # use random number generator to get frequency
    # get elapsed time formula: time = number_of_cycles / frequency
    # Init result dict to store values in
    results = {}

    # Create placeholder dict stuff
    for key in color_keys:
        results[key] = {}
        for col in non_prf_keys:
            results[key][col] = ""

    # Real World Data Collection [Change this when doing actual, test it]
    for key in color_keys:

        if key == RED_HEADER:
            # Get Red Data, freq and time
            freq, time = get_red_monotonic(number_of_cycles)
            pass
        elif key == GRN_HEADER:
            freq, time = get_green_monotonic(number_of_cycles)
            # Get Green Data, freq and time
            pass
        elif key == BLU_HEADER:
            freq, time = get_blue_monotonic(number_of_cycles)
            # Get Blue Data, freq and time
            pass
        elif key == CLR_HEADER:
            # Get Clear Data, freq and time
            freq, time = get_clear_monotonic(number_of_cycles)
            pass

        results[key][FREQ_HEADER] = freq
        results[key][TIME_HEADER] = time


    # Simulated Data Collection
    """
    for key in color_keys:

        freq = random.randint(8000, 24000)
        time = number_of_cycles / freq
        results[key][FREQ_HEADER] = freq
        results[key][TIME_HEADER] = time
    """

    # print(results)

    return results


def get_q1_data(number_of_trials):
    # Q1, data to collect:
    # - Number of cycles for RGBC, fixed. Cycles: 10, 100, 1000, 10k, 20k, 30k
    # - Elapsed time for RBC, same fixed cycles.
    # - Calculated: Frequency for RGBC: fixed cycles / elapsed time

    # Q1 Algorithm
    # Create list of fixed cycles to try
    # For loop to go through each element in fixed cycles
    for cycle in fixed_cycles:
        print("*****************")
        print(f"Non-PRF, Test Fixed Cycles: {cycle}")
        #   initialize empty list with 4 lists, to store elapsed time
        #   initialize empty list with 4 lists, to store calculated frequency
        #   Create dictionary of dictionaries to store data, use color_keys and non_prf_keys, call this non_prf_data_dict
        non_prf_data_dict = {}
        for color in color_keys:
            non_prf_data_dict[color] = {}
            for col in non_prf_keys:
                non_prf_data_dict[color][col] = []

        # print(non_prf_data_dict)
        # print(json.dumps(non_prf_data_dict, indent=4))
        #   For loop to go through 100 trials for that fixed cycles
        for i in range(number_of_trials):
            print(f"Trial {i}/{number_of_trials}")
            #  ****
            #  For the real one, change the line below
            #  ****
            #  Collect RGBC non-PRF
            row_dict = get_rgbc_non_prf(cycle)
            # pretty = json.dumps(row_dict, indent=4)
            # print(pretty)

            # Append to non_prf_data_dict
            for color in color_keys:
                for header in non_prf_keys:
                    current_data = row_dict[color][header]
                    non_prf_data_dict[color][header].append(current_data)
        #  Done with 100 trials
        #     print(json.dumps(non_prf_data_dict, indent=4))
        for color in color_keys:
            #   Turn all of those lists into columns for a dataframe,
            # print(f"Color: {color}")
            temp = non_prf_data_dict[color]
            df = pd.DataFrame(temp)
            # print(df)
            # Create Save file name
            # Filename Format: nonPRF_red_10_cycles.csv (number of trials is number of rows)
            save_filename = f"nonPRF_{color}_{cycle}_cycles.csv"
            # print(f"save_filename: {save_filename}")
            save_full_path = join(SAVE_FOLDER, save_filename)
            print(f"save_full_path: {save_full_path}")

            # Save to CSV
            df.to_csv(save_full_path)
    pass


def get_q2_data(number_of_trials):
    # Q2 Algorithm
    # Create list of fixed times to try
    # For loop to go through each element in fixed_times
    for time in fixed_times:
        print("*****************")
        print(f"PRF, Test Fixed Times: {time} seconds")
        # Create dictionary of dictionaries to store data, use color_keys and prf_keys, call this prf_data_dict
        prf_data_dict = {}
        for color in color_keys:
            prf_data_dict[color] = {}
            for header in prf_keys:
                prf_data_dict[color][header] = []

        # Print Placeholder/shell of prf_data_dict, pretty version
        # print(json.dumps(prf_data_dict, indent=4))
        #  For loop to go through 100 trials for that fixed time
        for i in range(number_of_trials):
            print(f"Trial {i}/{number_of_trials}")
            #  Collect RGBC PRF data and calculated data
            # ***** For Real World, Change the next line *****
            row_dict = get_rbgc_prf(time)
            for color in color_keys:
                for header in prf_keys:
                    #  use keys of collected data to match keys in prf_data_dict, store in lists with associated key
                    prf_data_dict[color][header].append(row_dict[color][header])
        #  Done with 100 trials

        # print(json.dumps(prf_data_dict, indent=4))
        #   Go through keys of prf_data_dict with for loop
        for color in color_keys:
            temp = prf_data_dict[color]
            # load data into dataframe
            df = pd.DataFrame(temp)
            # print(df)

            #  save to csv, filename format: PRF_red_1.0_seconds.csv
            save_filename = f"PRF_{color}_{time}_seconds.csv"
            save_full_path = join(SAVE_FOLDER, save_filename)
            print(f"save_full_path: {save_full_path}")

            # Save to CSV
            df.to_csv(save_full_path)
    pass


def main():
    
    color_sensor_setup()
    
    
    # Setup Output Frequency
    # set_100_output()
    # set_20_output()
    set_2_output()
    # set_power_down_output()
    
    print("Waiting 1 seconds for you to leave")
    
    time.sleep(1)
    
    number_of_trials = 100 # How many attempts to get RGBC frequency values.
    # Get Question 1 Data
    get_q1_data(number_of_trials)

    # Get Question 2 Data
    get_q2_data(number_of_trials)

    # time_to_wait = 1
    # get_rbgc_prf(time_to_wait)

    # number_of_cycles = 10
    # get_rgbc_non_prf(number_of_cycles)
    
    end_program()


    pass


if __name__ == "__main__":
    main()
