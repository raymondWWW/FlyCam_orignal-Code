"""
Play image folder as a "movie"

TODO: Display well number, date and time on image
TODO: Get time difference?
"""

import cv2

from datetime import datetime
from os import listdir
from os.path import isfile, join

IMAGE_FOLDER = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-22-2022\Code_Pictures_2022-07-21_194944'


def get_file_list(folder_path):
    file_list = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    return file_list


def filter_file_list(file_list):

    # Include only JPGs

    filtered_file_list = []

    for file in file_list:
        # print(file)
        parsed_str = file.split(sep=".")
        ext = parsed_str[-1]
        # print(parsed_str)

        # If file extension is jpg, add to filtered_file_list
        if ext == "jpg":
            filtered_file_list.append(file)
    # print(filtered_file_list)
    return filtered_file_list


def get_image_list(folder_path):

    file_list = get_file_list(folder_path)
    filtered_file_list = filter_file_list(file_list)
    return filtered_file_list


def maintain_aspect_ratio_resize_width(image, new_width):
    """
    Resize image maintaining aspect ratio of image using new_width

    :param image: An OpenCV image, a numpy 3D array. Format: original_height, original_width, channels
    :param new_width: An int, new width
    :return: Resized Image with correct aspect ratio.
    """

    if len(image.shape) == 3:
        # BGR or RGB Image, extract 3 variables
        original_height, original_width, channels = image.shape
    else:
        # Grayscale image, only 2 outputs
        original_height, original_width = image.shape

    # Calculate h2
    h2 = new_width * (original_height / original_width)

    # Round to nearest int
    new_height = round(h2)

    # Resize the Image
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


def get_date_and_time(filename):
    parsed_str = filename.split(sep="_")
    print(parsed_str)

    WELL = 0
    DATE = 1
    TIME = 0

    well_str = parsed_str[WELL]
    date_str = parsed_str[DATE]
    # Get last element, split based on period, then grab first element
    time_str = parsed_str[-1].split(sep=".")[TIME]

    print(time_str)

    # date_string = '2021-12-31 15:37'
    # date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    # print(date_obj)

    # date_string = '2022-07-21 194948'
    date_string = f"{date_str} {time_str}"
    date_obj = datetime.strptime(date_string, '%Y-%m-%d %H%M%S')
    print(date_obj)

    pass


def main2():
    filename = "well1_2022-07-21_194948.jpg"
    get_date_and_time(filename)


def main():
    print("main")
    folder_path = IMAGE_FOLDER
    file_list = get_image_list(folder_path)

    # Load first image
    image = cv2.imread(join(folder_path, file_list[0]))

    # TODO: Get resize factor, resize image, show selectROI, get crop box then change to resize factor
    # r = cv2.selectROI("select the area", image)
    # Well 1
    # x = 750
    # y = 230
    width = 2450
    height = 2490
    x0 = 750
    y0 = 230
    x1 = x0 + width
    y1 = y0 + height

    # Well 2:
    # x = 860
    # y = 250
    # w = 2450
    # h = 2340

    # Well 3
    # x = 890
    # y = 240
    # w = 2390
    # h = 2350

    # crop_image = image[y0:y1, x0:x1]


    # resized_image = maintain_aspect_ratio_resize_width(crop_image, new_width)
    # cv2.imshow("resized_image", resized_image)
    # cv2.waitKey(10000)

    # For loop through each file in file list
    for file in file_list:
        # load image as color
        image = cv2.imread(join(folder_path, file), cv2.IMREAD_COLOR)

        # Crop the image using ROI
        crop_image = image[y0:y1, x0:x1]

        # Resize image
        new_width = 640
        resized_image = maintain_aspect_ratio_resize_width(crop_image, new_width)

        # Display image
        cv2.imshow("resized_image", resized_image)

        # Wait x seconds
        cv2.waitKey(10)

    pass


if __name__ == "__main__":
    # main()
    main2()
