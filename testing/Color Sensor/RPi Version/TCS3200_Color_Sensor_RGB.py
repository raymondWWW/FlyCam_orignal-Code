"""
Color Sensor Code Tests

Variable Cycles, Fixed Time vs Fixed Cycles, Variable Time

Benchmark Tests Results from atman-iot.com
Rpi.GPIO: accurate up to 5 KHz, 50 KHz = Failed
PIGPIO: accurateup to 20 KHz, 110 KHz = Failed

Future Version: Learn and use PIGPIO


"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as GPIO
import time


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

NUM_CYCLES = 20000

# For PRF, time to wait in seconds
TIME_TO_WAIT = 1


def get_red_prf():
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    
    time_to_wait = TIME_TO_WAIT # in seconds

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


def get_green_prf():
    # GREEN: S2: HIGH, S3: HIGH
    # Set S2 and S3 to HIGH to capture green
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    
    time_to_wait = TIME_TO_WAIT # in seconds

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


def get_blue_prf():
    # BLUE: S2: LOW, S3: HIGH
    # Set S2 to LOW and S3 to HIGH to capture blue
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    
    time_to_wait = TIME_TO_WAIT # in seconds

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


def get_clear_prf():
    # CLEAR: S2: HIGH, S3: LOW
    # Set S2 to HIGH and S3 to LOW to capture clear
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    
    time_to_wait = TIME_TO_WAIT # in seconds

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


# Non-PRF, fixed cycles, variable time.
def get_red_monotonic():
    
    # RED: S2: LOW, S3: LOW
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    # print(f"RED: {red} Hz")
    return red


def get_green_monotonic():
    
    # GREEN: S2: HIGH, S3: HIGH
    # Set S2 and S3 to HIGH to capture green
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    green  = NUM_CYCLES / duration   #in Hz
    # print(f"green: {green} Hz")
    return green


def get_blue_monotonic():
    
    # BLUE: S2: LOW, S3: HIGH
    # Set S2 to LOW and S3 to HIGH to capture blue
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    blue  = NUM_CYCLES / duration   #in Hz
    # print(f"blue: {blue} Hz")
    return blue


def get_clear_monotonic():
    
    # CLEAR: S2: HIGH, S3: LOW
    # Set S2 to HIGH and S3 to LOW to capture clear
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.monotonic()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.monotonic() - start      #seconds to run for loop
    clear  = NUM_CYCLES / duration   #in Hz
    # print(f"clear: {clear} Hz")
    return clear


def get_red():
    
    # RED: S2: LOW, S3: LOW
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    # Get Start Time
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    # print(f"RED: {red} Hz")
    return red



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


# Calculation Stuff

def constrain(x_out, out_min, out_max):
    # Will constrain x_out to within the out min/max range
    result = x_out

    # If x_out is too low, make it out_min
    if x_out < out_min:
        result = out_min
    # else if x_out is too high, make out_max
    elif x_out > out_max:
        result = out_max

    return result


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range2(x, in_min, in_max, out_min, out_max):
    # map_range with Constrain

    # Init default value, which is just x. May need to change this for debugging.
    result = x

    # Calculate x in the output range
    x_out = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Constrain to the out min/max values, if needed
    # Will return x_out if not needed
    x_out_constrained = constrain(x_out, out_min, out_max)

    # Store x_out_constrained into result
    result = x_out_constrained

    return result


def map_range2_int(x, in_min, in_max, out_min, out_max):
    # map_range with Constrain

    # Init default value, which is just x. May need to change this for debugging.
    result = x

    # Calculate x in the output range
    x_out = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # Constrain to the out min/max values, if needed
    # Will return x_out if not needed
    x_out_constrained = constrain(x_out, out_min, out_max)

    # Store x_out_constrained into result after rounding and convert to int
    result = int(round(x_out_constrained))

    return result



def main():
    print("Main")
    
    global NUM_CYCLES, TIME_TO_WAIT
    
    end_program()
    
    color_sensor_setup()
    
    # Setup Output Frequency
    set_100_output()
    # set_20_output()
    # set_2_output()
    # set_power_down_output()
    time.sleep(3)
    
    # Channels, in BGR format
    B = 0; G = 1; R = 2
    
    height = 300
    width = 300
    channels = 3
    
    sample_box = np.zeros((height, width, channels),dtype='uint8') # black display
    
    data = [[], [], [], []]
    
    number_of_runs = 100
    NUM_CYCLES = 20000
    
    for i in range(number_of_runs):
        print(f"{i+1} / {number_of_runs}")
        """
        red = get_red_monotonic()
        grn = get_green_monotonic()
        blu = get_blue_monotonic()
        clr = get_clear_monotonic()
        
        
        row = [red, grn, blu, clr]
        
        for i in range(len(data)):
            # print(row[i])
            data[i].append(row[i])
        
        # print("*****")
        # print(f"Non-PRF: RED: {red:.2f}, GREEN: {grn:.2f}, BLUE: {blu:.2f}, CLEAR: {clr:.2f} Hz")
        
        """
        red_prf, _, _ = get_red_prf()
        grn_prf, _, _ = get_green_prf()
        blu_prf, _, _ = get_blue_prf()
        clr_prf, _, _ = get_clear_prf()
        
        print(f"____PRF: RED: {red_prf}, GREEN: {grn_prf}, BLUE: {blu_prf}, CLEAR: {clr_prf} Hz")
        
        
        
        r_dec = red_prf / clr_prf
        g_dec = grn_prf / clr_prf
        b_dec = blu_prf / clr_prf
        
        print(f"RGB (Dec): ({r_dec}, {g_dec}, {b_dec})")
        
        r = round(r_dec * 255)
        g = round(g_dec* 255)
        b = round(b_dec * 255)
        
        print(f"RGB from Norm (0-255): ({r}, {g}, {b})")
        sample_box[:, :, :] = [b, g, r]
        cv2.imshow("sample_box NORM", sample_box)
        # cv2.waitKey(1000)
        
        
        # Map Conversion to RGB (100%)
        r_map = map_range2_int(red_prf, 14000, 24000, 0, 255)
        g_map = map_range2_int(grn_prf, 8000, 19200, 0, 255)
        b_map = map_range2_int(blu_prf, 11200, 21600, 0, 255)
        
        print(f"RGB from Map: ({r_map}, {g_map}, {b_map})")
        sample_box[:, :, :] = [b_map, g_map, r_map]
        cv2.imshow("sample_box MAP", sample_box)
        
        cv2.waitKey(1000)
        
        
        
    
    end_program()
    
    """
    fig, axs = plt.subplots(1, len(data))
    
    titles = ["Red", "Green", "Blue", "Clear"]
    
    for i in range(len(data)):
        axs[i].boxplot(data[i])
        axs[i].set_title(f"{titles[i]} Frequency (Hz)")

    fig.suptitle(f"Non-PRF (Fixed Cycles, Variable Time)\nNumber of Cycles: {NUM_CYCLES}\nNumber of Runs: {number_of_runs}")
    
    plt.show()
    """
    
    """
    # PRF Tests, working code
    cycles = []
    dur_ext = []
    dur_int = []
    freq_ext = []
    freq_int = []
    
    red_mono_list = []
    for i in range(100):
        print(i)
        # PRF
        num_cycles, duration_external, elapsed_time = get_red_prf()
        cycles.append(num_cycles)
        dur_ext.append(duration_external)
        dur_int.append(elapsed_time)
        freq_ext.append(num_cycles/duration_external)
        freq_int.append(num_cycles/elapsed_time)
        
        # Fixed Cycles, Variable Time
        red_mono = get_red_monotonic()
        red_mono_list.append(red_mono)
    
    data = [dur_ext, dur_int]
    freq_data = [freq_ext, freq_int, red_mono_list]
    end_program()
    
    fig, axs = plt.subplots(1, 3)

    axs[0].boxplot(data)
    axs[0].set_title("Dur, Ext vs Int\n")


    axs[1].boxplot(cycles)
    axs[1].set_title("NumOfCycles")
    
    axs[2].boxplot(freq_data)
    axs[2].set_title("Freq, Ext vs Int vs non-PRF\n")

    plt.show()
    """
    
    """
    # Accuracy Tests, time.sleep vs time.monotonic, freq box plot
    red_list = []
    red_mono_list = []
    for i in range(100):
        red = get_red()
        red_list.append(red)
        
        red_mono = get_red_monotonic()
        red_mono_list.append(red_mono)
    end_program()
    
    # Delete first value since it is wrong?
    red_list.pop(0)
    red_mono_list.pop(0)
    
    data = [red_list, red_mono_list]
    
    plt.boxplot(data)
    plt.show()
    """
    
    """
    fig, axs = plt.subplots(1, 2)
    

    axs[0, 0].boxplot(data)
    axs[0, 0].set_title("time.sleep()")
    
    axs[0, 1].boxplot(data, 1)
    axs[0, 1].set_title("time.monotonic()")

    plt.show()
    """
    pass


if __name__ == "__main__":
    main()
