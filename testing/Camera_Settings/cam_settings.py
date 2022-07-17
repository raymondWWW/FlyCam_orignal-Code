"""
Sim Code to practice getting camera setting values:

Exposure: Digital/Analog Gain
AWB: Red/Blue Gains
Shutterspeed

Things to do:
-Change Metering Mode, view values above. Are they consistent?
-Get a consistent black image, get the above values.

Collect the above data in a CSV file?
Headers: Filename, digital gain, analog gain, red gain, blue gain, shutter speed



"""

import csv
import os
import random
import time

from datetime import datetime

# Save CSV Headers
HEADERS = ["file_name", "analog_gain", "digital_gain", "red_gain", "blue_gain", "shutter_speed"]

SAVE_CSV_FOLDER = r'D:\Projects\3dprinter_sampling\temp'
# SAVE_CSV_FILE gets updated by init_csv_file() (is temporary solution)
SAVE_CSV_FILE = ''


def get_unique_id():
    current_time = datetime.now()
    unique_id = current_time.strftime("%Y-%m-%d_%H%M%S")
    # print(f"unique_id: {unique_id}")
    return unique_id


def gen_cam_data(image_file_name):

    # Get Exposure Mode, Digital and Analog Gains
    analog_gain = random.random()
    digital_gain = random.random()

    # Get AWB, red and blue gains
    red_gain = random.random()
    blue_gain = random.random()

    # Get Shutterspeed
    shutter_speed = random.uniform(10.0, 35.0)

    data_row = [image_file_name, analog_gain, digital_gain, red_gain, blue_gain, shutter_speed]

    return data_row


def init_csv_file():

    global SAVE_CSV_FILE

    csv_file_name = f"cam_values_{get_unique_id()}.csv"

    SAVE_CSV_FILE = csv_file_name

    full_path = os.path.join(SAVE_CSV_FOLDER, csv_file_name)

    f = open(full_path, 'w', newline="")
    writer = csv.writer(f)
    writer.writerow(HEADERS)
    f.close()


def save_to_csv_file(data_row):

    full_path = os.path.join(SAVE_CSV_FOLDER, SAVE_CSV_FILE)

    # Append to existing CSV File
    f = open(full_path, 'a', newline="")

    writer = csv.writer(f)

    writer.writerow(data_row)

    f.close()
    print(f"File Updated: {full_path}")


def main():
    init_csv_file()
    image_file_name = f"image_{get_unique_id()}.jpg"

    data_row = gen_cam_data(image_file_name)
    print(data_row)
    save_to_csv_file(data_row)

    for i in range(10):
        save_to_csv_file(data_row)

    pass


if __name__ == "__main__":
    main()
