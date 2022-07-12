"""
Color Sensor Data Analysis

Make box plots to compare and answer these questions:

Q1: Increase precision of non-PRF by increasing fixed number of cycles?
Answer: It does, indeed. The IQR shrinks as it goes up, outliers also shrink too.

Q2: Decrease speed of PRF while maintaining precision by decreasing fixed time to wait?

Q2A: For both PRF and non-PRF best case scenario, do they have similar precision?
-What is similar precision? Small Variation? Similar Variation with box plot?

Q3: When switching to manual control of scaled output frequency, will 100% match previous setup?

Q4: How does precision change with 20% output? 2%? 100% is supposed to be the least accurate. Run same tests as Q1 and Q2.


Main Folder:
D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data
D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output

D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output\nonPRF
D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output\PRF

D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\new_pins

D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\new_pins\2_per

D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\new_pins\20_per

D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\new_pins\100_per


Code sources:
https://stackoverflow.com/questions/65354733/sort-a-list-of-file-names-numerically-in-python

"""

import matplotlib.pyplot as plt
import os
import pandas as pd

folder_prf = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output\PRF'
folder_non_prf = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output\nonPRF'
save_folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\7-6-2022\Data\100 Percent Output\Figures'


color_keys = ['red', 'blue', 'green', 'clear']

# nonPRF index
COLOR = 1
NUM_OF_CYCLES = 2


def main():
    print("main")

    # Q1, does nonPRF increase precision or smaller box plot with increased cycles?

    # Get list of files from nonPRF folder
    non_prf_list = [f for f in os.listdir(folder_non_prf) if os.path.isfile(os.path.join(folder_non_prf, f))]
    print(non_prf_list)

    non_prf_dict = {}
    non_prf_sorted_dict = {}
    for color in color_keys:
        non_prf_dict[color] = []
        non_prf_sorted_dict[color] = []
    print(non_prf_dict)
    # Sort files into dictionary of lists for those colors
    # go through each file in list
    for file in non_prf_list:
        # print(file)
        parsed_file_name = file.split(sep="_")
        # print(parsed_file_name)
        color_str = parsed_file_name[COLOR]
        # print(f"color: {color_str}")
        # cycles_str = parsed_file_name[NUM_OF_CYCLES]
        # print(f"cycles_str: {cycles_str}")
        non_prf_dict[color_str].append(file)
    #   split up file name
    #   get color
    #   get cycles (for practice)
    # print(non_prf_dict)

    print("Sort lists in dictiionary")
    for color, file_list in non_prf_dict.items():
        # print(f"{color}: {file_list}")
        nums = sorted([int(num.split('_')[NUM_OF_CYCLES]) for num in file_list]) #split the names and sort numbers
        # print(f"nums: {nums}")
        sorted_output = [ f"nonPRF_{color}_{cycles}_cycles.csv" for cycles in nums] #append file extension and create another list.
        print(f"sorted_output: {sorted_output}")
        non_prf_sorted_dict[color] = sorted_output

    print(non_prf_sorted_dict)

    freq_header = "frequency_(Hz)"

    MAX_ROW = 1
    MAX_COL = 6

    row = 0
    print("Starting Plot Extraction")
    for color, file_list in non_prf_sorted_dict.items():
        print(f"{color}: {file_list}")

        data_list = []
        col = 0
        fig, axs = plt.subplots(MAX_ROW, MAX_COL, constrained_layout=True, num=1, clear=True)
        # Initialize empty list of dataframes
        # Go through each file in file list
        for file in file_list:
            print(file)
            file_path = os.path.join(folder_non_prf, file)
            df = pd.read_csv(file_path)
            # data_list.append(df[freq_header])

            parsed_file_name = file.split(sep="_")
            color_str = parsed_file_name[COLOR]
            cycles_str = parsed_file_name[NUM_OF_CYCLES]

            axs[col].boxplot(df[freq_header])
            axs[col].set_title(f"{cycles_str} Cycles")
            #   Convert file to dataframe, extract frequency column

            fig.suptitle(f"{color_str} nonPRF")

            col += 1
        # plt.boxplot(data_list)
        # fig.suptitle(color_str)
        # mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()

        # plt.show(block=False)

        figure = plt.gcf()  # get current figure
        figure.set_size_inches(20, 11.25)  # set figure's size manually to your full screen (32x18)
        file_name = f'figure_nonPRF_{color}.png'
        save_full_path = os.path.join(save_folder, file_name)
        plt.savefig(save_full_path, bbox_inches='tight') # bbox_inches removes extra white spaces
        # fig.savefig(f"figure{row}.png")
        row += 1
        # break

    # file1 = non_prf_dict['red'][0]
    # file2 = non_prf_dict['red'][1]
    #
    # df1 = pd.read_csv(os.path.join(folder_non_prf, file1))
    # print(df1)
    #
    # df2 = pd.read_csv(os.path.join(folder_non_prf, file2))
    #
    # freq_header = "frequency_(Hz)"
    #
    # data = [df1[freq_header], df2[freq_header]]
    # plt.boxplot(data)
    # plt.show()
    pass


if __name__ == "__main__":
    main()
