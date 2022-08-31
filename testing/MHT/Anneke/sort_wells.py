"""
Sort Well Images into their own folder
Author: Johnny Duong
Creation Date: 8-31-2022


"""

import shutil

from os import listdir, mkdir
from os.path import isfile, isdir, join


def main():
    print("main")

    # Load full folder path
    # folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\dummy_folder'
    # folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2'
    folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\PH_08052022_ppMHT_ppMHTmCh_run2'

    # Get file list from folder path
    file_list = [f for f in listdir(folder) if isfile(join(folder, f))]
    print(file_list)

    well_names = []

    # Assume file names start with "well[x]"
    for file in file_list:
        # print(file)
        parsed_str = file.split(sep='_')
        # print(parsed_str)
        well_names.append(parsed_str[0])

    # Get unique starts
    well_names_unique = list(set(well_names))
    print(well_names_unique)

    # Make folder from unique starts, if it doesn't exist
    for well_name in well_names_unique:
        # print(well_name)

        new_folder_path = join(folder, well_name)

        if isdir(new_folder_path) == False:
            print(f"Making New Folder: {new_folder_path}")
            mkdir(new_folder_path)


    # Go through each file, move to that well folder.
    print("Sort well names into their folder")
    for file in file_list:
        parsed_str = file.split(sep='_')
        well_name = parsed_str[0]
        print(well_name)

        src = join(folder, file)
        print(f"src: {src}")
        dest = join(folder, well_name, file)
        print(f"dest: {dest}")

        shutil.move(src, dest)



    pass


if __name__ == "__main__":
    main()
