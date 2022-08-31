"""
Play image folder as a "movie"

TODO: Display well number, date and time on image
TODO: Get time difference?
TODO: Add black bars to maintain aspect ratio?

Code Sources:
https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior


Text on image
https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga5126f47f883d730f633d74f07456c576

LineTypes:
https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#gaf076ef45de481ac96e0ab3dc2c29a777

Code sources:

Working Images to Video:
http://www.scikit-video.org/stable/io.html
https://github.com/scikit-video/scikit-video/issues/98#issuecomment-411092932
https://stackoverflow.com/a/58371106


"""

import skvideo
skvideo.setFFmpegPath(r"D:\Audio\ffmpeg-4.3.2-2021-02-02-full_build\bin")

import cv2
import skvideo.io
import numpy as np

from datetime import datetime
from os import listdir
from os.path import isfile, join

# IMAGE_FOLDER = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-22-2022\Code_Pictures_2022-07-21_194944'

IMAGE_FOLDER = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-28-2022\Code_Pictures_2022-08-24_181456\Well1'

SAVE_FOLDER = r'D:\Projects\3dprinter_sampling\testing\Image_Processing\cropped'

WELL_KEY = "well_number"
DATE_KEY = "datetime"


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


def maintain_aspect_ratio_resize_height(image, new_height):
    """
    Resize image maintaining aspect ratio of image using new_width

    :param image: An OpenCV image, a numpy 3D array. Format: original_height, original_width, channels
    :param new_height: An int, new height
    :return: Resized Image with correct aspect ratio.
    """

    original_height, original_width, channels = image.shape

    # Calculate h2
    w2 = new_height * (original_width / original_height)

    # Round to nearest int
    new_width = round(w2)

    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


def get_filename_data(filename):
    result = {}

    parsed_str = filename.split(sep="_")
    # print(parsed_str)

    WELL = 0
    DATE = 1
    TIME = 0

    well_str = parsed_str[WELL]
    date_str = parsed_str[DATE]
    # Get last element, split based on period, then grab first element
    time_str = parsed_str[-1].split(sep=".")[TIME]

    # print(time_str)

    # date_string = '2021-12-31 15:37'
    # date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    # print(date_obj)

    # date_string = '2022-07-21 194948'
    date_string = f"{date_str} {time_str}"
    date_obj = datetime.strptime(date_string, '%Y-%m-%d %H%M%S')
    # print(date_obj)
    # print(date_obj.strftime("%A, %d. %B %Y %I:%M%p"))

    # Grab well number only, the 4th character to the end.
    # Should help if the well number is more than 1 digit.
    result[WELL_KEY] = well_str[4:]
    result[DATE_KEY] = date_obj

    # print(result)
    return result


def main4():

    folder_path = IMAGE_FOLDER
    file_list = get_image_list(folder_path)
    counter = 0
    for file in file_list:
        print(f"Image {counter} / {len(file_list)}")
        image = cv2.imread(join(folder_path, file), cv2.IMREAD_COLOR)
        frame = cv2.resize(image, (640, 480))

        cv2.imshow("frame", frame)
        cv2.waitKey(10)
        counter += 1

    cv2.destroyAllWindows()

    pass


def main3():
    # Note: This method does not work, empty video is created
    # Save images as video only
    print("main3")
    folder_path = IMAGE_FOLDER
    file_list = get_image_list(folder_path)

    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # out = cv2.VideoWriter('SaveVideo3.avi', fourcc, 20.0, (480, 640), isColor=False)

    width = 640
    height = 480

    # out_video = np.empty([40, height, width, 3], dtype=np.uint8)
    out_video = np.empty([len(file_list), height, width, 3], dtype=np.uint8)
    out_video = out_video.astype(np.uint8)

    counter = 0
    # For loop through each file in file list
    for file in file_list:
        print(f"Image {counter} / {len(file_list)}")

        # if counter >= 40:
        #     break

        # load image as color
        image = cv2.imread(join(folder_path, file), cv2.IMREAD_COLOR)
        frame = cv2.resize(image, (640, 480))

        out_video[counter] = frame

        # out.write(frame)

        counter += 1

    # out.release()
    # Writes the the output image sequences in a video file
    skvideo.io.vwrite("video.mp4", out_video)

    cv2.destroyAllWindows()

    pass


def main2():
    filename = "well1_2022-07-21_194948.jpg"
    get_filename_data(filename)


def main():
    print("main")
    folder_path = IMAGE_FOLDER
    file_list = get_image_list(folder_path)

    # Load first image
    image = cv2.imread(join(folder_path, file_list[0]))

    # TODO: Get resize factor, resize image, show selectROI, get crop box then change to resize factor
    # r = cv2.selectROI("select the area", image)

    # D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-28-2022\Code_Pictures_2022-08-24_181456\Well1
    # No sample, hardware test
    # width = 2340
    # height = 2370
    # x0 = 850
    # y0 = 340
    # x1 = x0 + width
    # y1 = y0 + height

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

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (10, 30)

    # fontScale
    fontScale = 1

    # Blue color in BGR
    # color = (255, 0, 0)
    color = (86, 236, 247)

    # Line thickness of 2 px
    thickness = 2

    line_type = cv2.LINE_AA

    # Using cv2.putText() method

    # Video Stuff
    frame_width = 640
    frame_height = 480

    # frame_width = 2450
    # frame_height = 2490 + 100

    # video_fps = 20.0
    # four_cc = cv2.VideoWriter_fourcc(*'MJPG')
    # four_cc = -1
    # output = cv2.VideoWriter('output2.avi', four_cc, video_fps, (frame_height, frame_width), isColor=False)

    width = 640
    height = 480

    out_video = np.empty([40, height, width, 3], dtype=np.uint8)
    out_video = out_video.astype(np.uint8)

    counter = 0
    # For loop through each file in file list
    for file in file_list:

        print(f"Image {counter} / {len(file_list)}")

        # if counter == 40:
        #     break

        # Get well number and date/time from filename
        filename_data_dict = get_filename_data(file)

        # load image as color
        image = cv2.imread(join(folder_path, file), cv2.IMREAD_COLOR)

        # Crop the image using ROI

        yeast = ""

        if filename_data_dict[WELL_KEY] == "1":
            # 75 uL
            yeast = "75 uL"
            width = 2450
            height = 2490 + 100
            x0 = 750
            y0 = 150
            x1 = x0 + width
            y1 = y0 + height
        elif filename_data_dict[WELL_KEY] == "2":
            # 85 uL
            yeast = "85 uL"
            x0 = 860
            y0 = 150
            w = 2450
            h = 2340 + 100
            x1 = x0 + w
            y1 = y0 + h
        elif filename_data_dict[WELL_KEY] == "3":
            # 90 uL
            yeast = "90 uL"
            x0 = 890
            y0 = 140
            w = 2390
            h = 2350 + 100
            x1 = x0 + w
            y1 = y0 + h

        crop_image = image[y0:y1, x0:x1]

        # Resize image
        # new_width = 640
        # resized_image = maintain_aspect_ratio_resize_width(crop_image, new_width)

        new_height = 1080
        resized_image = maintain_aspect_ratio_resize_height(crop_image, new_height)

        image_text = f"Well {filename_data_dict[WELL_KEY]} ({yeast}), {filename_data_dict[DATE_KEY]}"

        resized_image = cv2.putText(resized_image, image_text, org, font,
                            fontScale, color, thickness, line_type)


        # Save Image

        # Create filename
        save_file_name = f"well_{filename_data_dict[WELL_KEY]}_{counter}.jpg"

        # Save to specific folder
        save_full_path = join(SAVE_FOLDER, save_file_name)

        # Save image
        cv2.imwrite(save_full_path, resized_image)

        # --- START VIDEO SAVE ---
        # Working Image to Video Save, but resize is restricting. Need to figure out how to add black borders to maintain aspect ratio
        # TODO: Save 3 different videos for 3 different wells
        # frame = cv2.resize(resized_image, (frame_width, frame_height))
        #
        # # Swap BGR to RGB
        # frame_copy = frame.copy()
        #
        # frame_copy[:, :, 0] = frame[:, :, 2]
        # frame_copy[:, :, 2] = frame[:, :, 0]
        #
        # out_video[counter] = frame_copy

        # --- END VIDEO SAVE ---

        # cv2.imshow("frame", frame)
        # output.write(frame)


        # Display image
        # cv2.imshow("resized_image", resized_image)

        # Wait x seconds
        # cv2.waitKey(250)
        counter += 1

    # Out of loop
    cv2.destroyAllWindows()
    # output.release()

    skvideo.io.vwrite("video2.mp4", out_video)

    pass


if __name__ == "__main__":
    # main()
    # main2()
    main3()
    # main4()
