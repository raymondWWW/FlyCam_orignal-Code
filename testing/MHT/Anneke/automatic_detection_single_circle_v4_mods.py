"""

TODO:
-Get folder name from image folder (not well)
-Use folder name as prefix for save RGB/HSV CSV files
-Put selection dim on selection image
-Figure out curve_fit?
-Bonus: do selection image for first and last image

"""

###room for improvement
# error carching, do not process images withou correct circle detection



from PIL.Image import Image as PilImage
import textwrap, os
import math 
import numpy as np
import cv2
import matplotlib.pyplot as plt # for plotting histogram
import os
import string
import pandas as pd

from datetime import datetime
from itertools import product
from numpy import pi, sin, linspace, exp, polyfit
from matplotlib.pyplot import figure, show
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
well="well"
thresh=110
blur=7
h=[]
s=[]
v=[]

r=[]
g=[]
b=[]
date=[]
counter=0
images=[]
#####min and max radius for circle detection
###for one well per image approx
minR = 100
maxR= 110
###for all wells
#minR= 50
#maxR= 150

###img dimension
xdim= 600 #480
ydim= 400 #640
rrxn=[]
rrxnlist0=[]
rrxnlist=[]
# take all files from a certain well
# folder=r'/Users/patraholmes/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Research Lab/MHT project/PH_08132022_200ulPNPA_1800ulBuffer_nolight_12wellblkplate'
#folder=r'C:/Users/Familie Moeller/Desktop/Files/College/SFSU/Independent Study/Dr.E Lab/Colorimetric Assay Data/02222022 Data/02222022 Data/MHT_022222_PH_Run01'
#folder=r'C:/Users/Familie Moeller/Desktop/Files/College/SFSU/Independent Study/Dr.E Lab/MHT Pictures/MHT Pictures/6-9-2021 (Wed)/Code_Pictures_2021-06-09_034320'
# folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-15-2022\RoboCam\MHT\PH_08082022_stdassay_run2'
# folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-15-2022\RoboCam\MHT\PH_08122022_PNPA_pHdep_Assay_run01'
# folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-15-2022\RoboCam\MHT\PH_08122022_PNPA_pHdep_Assay_run01_temp'
# folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-15-2022\RoboCam\MHT\PH_08132022_200ulPNPA_1800ulBuffer_nolight_12wellblkplate'
# folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\08302022_200ulPNPA_1800ulbuffer_run3_focused\Well2'
# folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2\well6'
folder = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\PH_08052022_ppMHT_ppMHTmCh_run2\well12'

isFirstTime = True
x1, y1, x2, y2 = 0, 0, 0, 0

folder_data_headers = ["data_name", "well_name", "save_folder"]
DATA_NAME = folder_data_headers[0]
WELL_NAME = folder_data_headers[1]
SAVE_FOLDER = folder_data_headers[2]


def get_folder_data(folder_path):
    # Assumes string format: D:\Documents\SF State\Dr. E Lab\MHT\Data\08302022_200ulPNPA_1800ulbuffer_run3_focused\Well2
    # Get folder name, not the well2
    dest_index = -2
    parsed_str = folder_path.split(sep="\\")
    data_name = parsed_str[dest_index]
    print(f"data_name: {data_name}")
    well_name = parsed_str[-1]
    print(f"well_name: {well_name}")
    save_folder = f"D:\\"
    # Go through parsed_str, create new save folder, but exclude well_name
    parsed_str_len = len(parsed_str)
    for i in range(1, parsed_str_len - 1):
        save_folder = os.path.join(save_folder, parsed_str[i])
    print(f"save_folder: {save_folder}")
    result = {'data_name': data_name, "well_name": well_name, "save_folder": save_folder}
    return result


# Test code for get_folder_data()
# folder_path = r'D:\Documents\SF State\Dr. E Lab\MHT\Data\8-31-2022\08312022_MeI_stds_run2\well1'
folder_data = get_folder_data(folder)
# print(folder_data)


for file in os.listdir(folder):
    if file.startswith(well):
        if file.endswith(".jpg"):
            img= cv2.imread(os.path.join(folder, file))
            #nimg+=1            
            name=os.path.splitext(file)[0]
            split_string=name.split('_', 1)
            split=split_string[1].rsplit('_', 1)
            n = 2
            time = [split[1][i:i+n] for i in range(0, len(split[1]), n)]
            hours = ((int(time[0])*60)*60)
            minute= (int(time[1])*60)
            seconds=int(time[2])
            rrxn =(hours+minute+seconds)
            rrxnlist0=np.append(rrxnlist0, rrxn)

            
        if img is not None:
            print('image found')

            s_img = cv2.resize(img, (320, 240))


            rgbblurIM=cv2.GaussianBlur(s_img, (5, 5), 0)
            # cv2.imshow('rgbblurIM crop', rgbblurIM[184:184+27, 74:74+21]) #best results
            # print('rgbblurIM Datatype:', rgbblurIM.dtype)


            img_copy=s_img.copy()
            hsvImg= cv2.cvtColor(s_img,cv2.COLOR_BGR2HSV)
            blurHSVIM= cv2.GaussianBlur(hsvImg, (5, 5), 0)
            grayIM = cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)     # convert color to grayscale image
            blurIM=cv2.GaussianBlur(grayIM, (5, 5), 0)
            #cv2.imshow('blur', blurIM)
            wide = cv2.Canny(blurIM, 10, 200)
            mid = cv2.Canny(blurIM, 30, 150)
            tight = cv2.Canny(blurIM, 240, 250)
            # cv2.imshow('blurHSVIM', blurHSVIM) #best results
            # cv2.imshow('wide', wide) #best results
            #cv2.imshow('mid', mid) #best results
            #cv2.imshow('tight', tight) #best results

            # print('blurHSVIM Datatype:', blurHSVIM.dtype)

            if isFirstTime:
                # Allow user to select ROI
                # Select ROI
                # r = cv2.selectROI("select the area", s_img)
                # print(f"r: {r}")
                x1, y1, x2, y2 = (127, 90, 76, 69)
                # # Get coordinates
                # tes of ROI
                # x1, y1, x2, y2 = r

                # x1, y1, x2, y2 = (122, 74, 88, 74)


                # 08302022_200ulPNPA_1800ulbuffer_run3_focused\Well1
                # (131, 94, 109, 79)
                # x1 = 131
                # y1 = 94
                # x2 = 109
                # y2 = 79

                # 08302022_200ulPNPA_1800ulbuffer_run3_focused\Well2
                # r: (148, 102, 64, 59)
                # x1 = 131
                # y1 = 94
                # x2 = 109
                # y2 = 79
                # x1, y1, x2, y2 = (148, 102, 64, 59)

                # 08302022_200ulPNPA_1800ulbuffer_run3_focused\Well3
                # (131, 90, 106, 81)
                # x1 = 131
                # y1 = 90
                # x2 = 106
                # y2 = 81

                # 08302022_200ulPNPA_1800ulbuffer_run3_focused\Well4
                # (160, 108, 57, 53)
                # x1 = 160
                # y1 = 108
                # x2 = 57
                # y2 = 53

                # PH_08122022_PNPA_pHdep_Assay_run01
                # x1 = 187
                # y1 = 74
                # x2 = 19
                # y2 = 22

                # PH_08132022_200ulPNPA_1800ulBuffer_nolight_12wellblkplate
                # Right Image
                # r: (186, 139, 43, 36)
                # x1 = 185
                # y1 = 137
                # x2 = 43
                # y2 = 36

                # Left Image
                # r: (106, 139, 44, 32)
                # x1 = 106
                # y1 = 139
                # x2 = 44
                # y2 = 32

                # Draw selection rectangle on image and save it.
                # Start coordinate, here (100, 50)
                # represents the top left corner of rectangle
                start_point = (x1, y1)

                # Ending coordinate, here (125, 80)
                # represents the bottom right corner of rectangle
                end_point = (x1+x2, y1+y2)

                # Black color in BGR
                color = (0, 0, 255)

                # Line thickness of -1 px
                # Thickness of -1 will fill the entire shape
                thickness = 2

                # Using cv2.rectangle() method
                # Draw a rectangle of black color of thickness -1 px
                s_img_rect = cv2.rectangle(img_copy, start_point, end_point, color, thickness)
                # cv2.imshow("s_img_rect", s_img_rect)
                # cv2.waitKey(10000)

                save_filename = f"{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_sample_image.png"
                save_full_path = os.path.join(folder_data[SAVE_FOLDER], save_filename)

                cv2.imwrite(save_full_path, s_img_rect)
                print(f"Saved image to: {save_full_path}")

                # Create and save image with selection shown.

                isFirstTime = False


            # r = cv2.selectROI("select the area", s_img)
            # print(f"r: {r}")

            # Get coordinates of ROI
            # x0, y0, w, h = r
            # x0 = int(x0)
            # y0 = int(y0)
            # w = int(w)
            # h = int(h)

            # PH_08122022_PNPA_pHdep_Assay_run01
            # x1 = 187
            # y1 = 74
            # x2 = 19
            # y2 = 22

            # Crop image
            # cropped_image = s_img[int(r[1]):int(r[1]+r[3]),
            #                       int(r[0]):int(r[0]+r[2])]
            cropped_image = s_img[y1:y1+y2, x1:x1+x2, :]

            # Display cropped image
            # cv2.imshow("Cropped image", cropped_image)
            # cv2.waitKey(0)

            # Using s_image, get blue, green and red channels as separate images
            blueIM=s_img[:,:,0]                   # b,g,r
            greenIM=s_img[:,:,1]
            redIM=s_img[:,:,2]

            # cv2.imshow('blue',blueIM)
            # cv2.waitKey(10000)

            # Crop blurHSVIM to ROI
            # print(f"blurHSVIM.shape: {blurHSVIM.shape}")
            blurHSVIM_cropped = blurHSVIM[y1:y1+y2, x1:x1+x2, :]
            #   Extract h channel, store in hi
            hi = blurHSVIM_cropped[:, :, 0]

            #   Get average of hi, store in h numpy array
            h=np.append(h, int(np.average(hi)))
            # h.append(int(np.average(hi)))

            #   Extract s channel, store in si
            si = blurHSVIM_cropped[:, :, 1]
            #   Get average of si, store in s numpy array
            s=np.append(s,int(np.average(si)))
            # print(f"s: {s}")

            #   Extract v channel, store in vi
            vi = blurHSVIM_cropped[:, :, 2]
            #   Get average of vi, store in v numpy array
            v=np.append(v, int(np.average(vi)))

            #   Do the same with RGB
            # Crop rgbblurIM
            # print(f"rgbblurIM.shape: {rgbblurIM.shape}")
            rgbblurIM_cropped = rgbblurIM[y1:y1+y2, x1:x1+x2, :]
            #

            # x0 = 187
            # y0 = 74
            # w = 19
            # h = 22

            ri = rgbblurIM_cropped[:, :, 2]
            r=np.append(r, int(np.average(ri)))
            #
            gi = rgbblurIM_cropped[:, :, 1]
            g=np.append(g,int(np.average(gi)))
            #
            bi = rgbblurIM_cropped[:, :, 0]
            b=np.append(b, int(np.average(bi)))





            # print(v)

            """
          ########## find circle in image ##########
            #with sharpie: param 1: 100, param 2: 15
            #without sharpie: param 1: 65, param 2: 10
            circles=cv2.HoughCircles(wide, cv2.HOUGH_GRADIENT, 1,120, param1=68, param2=15, minRadius=minR, maxRadius=maxR)
            circles=np.uint16(np.around(circles))
            for i in circles[0, :]:
                if circles.shape[1]<1:
                    print('not enough circles')
                    continue
                radius = i[2]-50
          ####### draw circle in image #######################
                #outer circles
                cv2.circle(img_copy, (i[0], i[1]), i[2], (0, 255, 2), 2)
                square=img_copy[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 2]=255

                # TODO: Find out what happens to this img_copy
                cv2.imshow('draw circle', img_copy)

                
                images.append(img_copy)

                blueIM=s_img[:,:,0]                   # b,g,r
                greenIM=s_img[:,:,1]
                redIM=s_img[:,:,2]
                #cv2.imshow('blue',blueIM)
                #cv2.imshow('green',greenIM)
               # cv2.imshow('red',redIM)
                cv2.imshow('colorIM',s_img)

                
                
         ########### get HSV and RGB values of the circle ##########
                    #for i in range(len(points[0, :])):
                hi = blurHSVIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 0] #2W by 2W HSV img
                h=np.append(h, int(np.average(hi)))
                #print('h', h)
                si = blurHSVIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 1] #2W by 2W HSV img   
                s=np.append(s,int(np.average(si)))
                vi = blurHSVIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 2] #2W by 2W HSV img
                v=np.append(v, int(np.average(vi)))
                #print('h ', h,'s ', s,'v ',  v)


                ri = rgbblurIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 2] #2W by 2W HSV img
                r=np.append(r, int(np.average(ri)))
                gi = rgbblurIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 1] #2W by 2W HSV img   
                g=np.append(g,int(np.average(gi)))
                bi = rgbblurIM[i[1]-30:i[1]+30, i[0]-30:i[0]+30, 0] #2W by 2W HSV img
                b=np.append(b, int(np.average(bi)))
                #cv2.imshow('resized Image', s_img)
            """
for i in range(len(rrxnlist0)):
    i=int(i)
    rrxnli=(int(rrxnlist0[i]-int(rrxnlist0[0])))
    rrxnlist=np.append(rrxnlist, rrxnli)


hn=[]
for i in range(len(h)):
    if h[i]-h[i-2]!=0:
        hn=np.append(hn, h[i])
    else:
        break
sn=[]
for i in range(len(s)):
    print(s[i]-s[i-2])
    # TODO: Line 337, Originally 3, changed 1
    if abs(s[i]-s[i-2])>1:
        sn=np.append(sn, s[i])
    else:
        break
vn=[]
for i in range(len(v)):
    if v[i]-v[i-2]!=0:
        vn=np.append(vn, v[i])
    else:
        break
print('sn', sn, 'hn', hn, 'vn', vn)

rn=[]
for i in range(len(r)):
    if r[i]-r[i-2]!=0:
        rn=np.append(rn, r[i])
    else:
        break
gn=[]
for i in range(len(g)):
    print(g[i]-g[i-2])
    if abs(g[i]-g[i-2])>6:
        gn=np.append(gn, g[i])
    else:
        break
bn=[]
for i in range(len(b)):
    if b[i]-b[i-2]!=0:
        bn=np.append(bn, b[i])
    else:
        break
print('sn', sn, 'hn', hn, 'vn', vn)
print('rn', rn, 'gn', gn, 'bn', bn)


##plt.plot(rrxnlist[:len(hn)], hn)
##plt.plot(rrxnlist[:len(sn)], sn)
##plt.plot(rrxnlist[:len(vn)], vn)
##plt.show()
vlinerrxnlist=rrxnlist[:len(vn)]
slinerrxnlist=rrxnlist[:len(sn)]

plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('font', weight='bold')
fig, ax = plt.subplots()
##ax.xaxis.set_minor_locator(minorLocator)
##ax.yaxis.set_minor_locator(minorLocator)

#ax.plot(rrxnlist[:len(hn)], hn, label='H',  color='purple')
ax.plot(rrxnlist[:len(sn)], sn, label='S', color='blue')
#ax.plot(rrxnlist[:len(vn)], vn, label='V', color='orange')
##ax.tick_params(which='both', width=2)
##ax.tick_params(which='major', length=7

# # Linear Fit Plot
# coefficient_v= np.polyfit(rrxnlist[:len(sn)], sn, 1)
# poly_v= np.poly1d(coefficient_v)
# new_x_v = np.linspace(slinerrxnlist[0], slinerrxnlist[-1])
# new_y_v = poly_v(new_x_v)
# ax.plot(new_x_v, new_y_v, label='linear fit', color="black")
# print('equation: ', poly_v)
# vx= (v[1]-poly_v[1])/poly_v[0]
# print('x value in v: ', vx)
#
# ax.minorticks_on()
# ax.tick_params(which='minor', length=4)
#
#
# plt.xlabel('time (s)')
# plt.ylabel('Saturation')
# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=6, fontsize ='large')
# plt.tight_layout()
# plt.savefig(f"{folder_data[SAVE_FOLDER]}\{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_linear_fit")

# plt.show()


def display_images(
    images: [PilImage], 
    columns=5, width=20, height=8, max_images=36, 
    label_wrap_length=50, label_font_size=8):

    if not images:
        print("No images to display.")
        return 

    if len(images) > max_images:
        print(f"Showing {max_images} images of {len(images)}:")
        images=images[0:max_images]

    height = max(height, int(len(images)/columns) * height)
    plt.figure(figsize=(width, height))
    for i, image in enumerate(images):

        plt.subplot(int(len(images) / columns + 1), columns, i + 1)
        plt.imshow(image)
    plt.show()
                
display_images(images)
        ##    

#cv2.imshow('Circle Detection', s_img)
#plt.title(well)
#plt.subplot(1, 2, 1)
##minorLocator = AutoMinorLocator()
plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('font', weight='bold')
fig, ax = plt.subplots()
##ax.xaxis.set_minor_locator(minorLocator)
##ax.yaxis.set_minor_locator(minorLocator)

# print(f"rrxnlist.shape: {rrxnlist.shape}")
# print(f"h.shape: {h.shape}")

ax.plot(rrxnlist, h, label='H',  color='purple')
ax.plot(rrxnlist, s, label='S', color='black')
ax.plot(rrxnlist, v, label='V', color='orange')
##ax.tick_params(which='both', width=2)
##ax.tick_params(which='major', length=7)
ax.minorticks_on()
ax.tick_params(which='minor', length=4)

plt.xlabel('time (s)')
plt.ylabel('HSV')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=6, fontsize ='large')
plt.tight_layout()
plt.savefig(f"{folder_data[SAVE_FOLDER]}\{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_hsv")
# plt.show()

#plt.subplot(1, 2, 2)
fig, ax = plt.subplots()
plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('font', weight='bold')
plt.plot(rrxnlist, r, label='R',  color='red')
plt.plot(rrxnlist, g, label='G', color='green')
plt.plot(rrxnlist, b, label='B', color='blue')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=6)
##ax.tick_params(which='major', length=7)
ax.minorticks_on()
ax.tick_params(which='minor', length=4)
plt.xlabel('time (s)')
plt.ylabel('RGB')
#plt.title(split_string[1]+'_' + well )
plt.tight_layout()
# plt.savefig(split_string[1] + well)
plt.savefig(f"{folder_data[SAVE_FOLDER]}\{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_rgb")
# plt.show()

# DATA_NAME = folder_data_headers[0]
# WELL_NAME = folder_data_headers[1]
# SAVE_FOLDER = folder_data_headers[2]

# TODO:
# Save to CSV
# h=[]
# s=[]
# v=[]
#
# r=[]
# g=[]
# b=[]

# Put in time stamp

# Create RGB data dict
rgb_dict = {"time": rrxnlist, "r": r, "g": g, "b": b}

# Create HSV data dict
hsv_dict = {"time": rrxnlist, "h": h, "s": s, "v": v}

# print(rgb_dict)
# print(hsv_dict)

# Create dataframes
df_rgb = pd.DataFrame(rgb_dict)
df_hsv = pd.DataFrame(hsv_dict)

# DATA_NAME = folder_data_headers[0]
# WELL_NAME = folder_data_headers[1]
# SAVE_FOLDER = folder_data_headers[2]

# Create save file name for RGB and HSV
# folder_data = get_folder_data(folder)
rgb_save_name = f"{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_rgb_data.csv"
hsv_save_name = f"{folder_data[DATA_NAME]}_{folder_data[WELL_NAME]}_hsv_data.csv"

rgb_full_save_path = os.path.join(folder_data[SAVE_FOLDER], rgb_save_name)
hsv_full_save_path = os.path.join(folder_data[SAVE_FOLDER], hsv_save_name)

# Save CSV files
df_rgb.to_csv(rgb_full_save_path)
df_hsv.to_csv(hsv_full_save_path)

print(f"CSV Saved: {rgb_full_save_path}")
print(f"CSV Saved: {hsv_full_save_path}")

# Linear Fit
# y=s
# x=rrxnlist
#
# num_points = len(x)
#
# min_fit_length = 100
#
# chi = 0
#
# chi_min = 10000
#
# i_best = 0
# j_best = 0
#
# for i in range(len(x) - min_fit_length):
#    for j in range(i+min_fit_length, len(x)):
#
#        coefs = polyfit(x[i:j],y[i:j],1)
#        y_linear = x * coefs[0] + coefs[1]
#        chi = 0
#        for k in range(i,j):
#            chi += ( y_linear[k] - y[k])**2
#
#        if chi < chi_min:
#            i_best = i
#            j_best = j
#            chi_min = chi
#            print(chi_min)
#
# coefs = polyfit(x[i_best:j_best],y[i_best:j_best],1)
# y_linear = x[i_best:j_best] * coefs[0] + coefs[1]
#
#
# fig = figure()
# ax = fig.add_subplot(111)
# ax.plot(x,y,'ro')
# ax.plot(x[i_best:j_best],y_linear,'b-')
# plt.show()
#
