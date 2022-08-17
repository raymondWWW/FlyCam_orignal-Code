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
from datetime import datetime
from itertools import product
from numpy import pi, sin, linspace, exp, polyfit
from matplotlib.pyplot import figure, show
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
well="well1"
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
folder = r'D:\Documents\SF State\Dr. E Lab\Spring 2022\RoboCam\8-15-2022\RoboCam\MHT\PH_08122022_PNPA_pHdep_Assay_run01'

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

            img_copy=s_img.copy()
            hsvImg= cv2.cvtColor(s_img,cv2.COLOR_BGR2HSV)
            blurHSVIM= cv2.GaussianBlur(hsvImg, (5, 5), 0)
            grayIM = cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)     # convert color to grayscale image
            blurIM=cv2.GaussianBlur(grayIM, (5, 5), 0)
            #cv2.imshow('blur', blurIM)
            wide = cv2.Canny(blurIM, 10, 200)
            mid = cv2.Canny(blurIM, 30, 150)
            tight = cv2.Canny(blurIM, 240, 250)
            cv2.imshow('wide', wide) #best results
            #cv2.imshow('mid', mid) #best results
            #cv2.imshow('tight', tight) #best results





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
    if abs(s[i]-s[i-2])>3:
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

coefficient_v= np.polyfit(rrxnlist[:len(sn)], sn, 1)
poly_v= np.poly1d(coefficient_v)
new_x_v = np.linspace(slinerrxnlist[0], slinerrxnlist[-1])
new_y_v = poly_v(new_x_v)
ax.plot(new_x_v, new_y_v, label='linear fit', color="black")
print('equation: ', poly_v)
vx= (v[1]-poly_v[1])/poly_v[0]
print('x value in v: ', vx)

ax.minorticks_on()
ax.tick_params(which='minor', length=4)


plt.xlabel('time (s)')
plt.ylabel('Saturation')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=6, fontsize ='large')


plt.show()




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
plt.show()

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
plt.savefig(split_string[1] + well)
plt.show()

##y=s
##x=rrxnlist
##
##num_points = len(x)
##
##min_fit_length = 100
##
##chi = 0
##
##chi_min = 10000
##
##i_best = 0
##j_best = 0
##
##for i in range(len(x) - min_fit_length):
##    for j in range(i+min_fit_length, len(x)):
##
##        coefs = polyfit(x[i:j],y[i:j],1)
##        y_linear = x * coefs[0] + coefs[1]
##        chi = 0
##        for k in range(i,j):
##            chi += ( y_linear[k] - y[k])**2
##
##        if chi < chi_min:
##            i_best = i
##            j_best = j
##            chi_min = chi
##            print(chi_min)
##
##coefs = polyfit(x[i_best:j_best],y[i_best:j_best],1)
##y_linear = x[i_best:j_best] * coefs[0] + coefs[1]
##
##
##fig = figure()
##ax = fig.add_subplot(111)
##ax.plot(x,y,'ro')
##ax.plot(x[i_best:j_best],y_linear,'b-')
##plt.show()

