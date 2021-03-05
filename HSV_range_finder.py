# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:31:35 2020

@author: Om Patel
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys

pointsX = []
pointsY = []

#   c:\development\projects\drone
#   frame 2493.jpg

img_path = input("put image path: ")
img_name = input(f"put image name in path {img_path}: ")

img = cv2.imread(f'{img_path}\{img_name}')

def mousePosition( event,x,y,flags,param):
    
    imgCopy = img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN:    
        pointsX.append(x) 
        pointsY.append(y)
    if event == cv2.EVENT_RBUTTONDOWN:
        pointsX.pop()
        pointsY.pop()
    if len(pointsX) == 1:
        
        cv2.rectangle(imgCopy, (pointsX[0],pointsY[0]), (x,y), (255,0,0), 2)
        
    elif len(pointsX) == 2:
        
        cv2.rectangle(imgCopy, (pointsX[0],pointsY[0]), (pointsX[1],pointsY[1]), (255,0,0), 2)
        
    elif len(pointsX) > 2:
        pointsX.pop()
        pointsY.pop()
    cv2.imshow('image',imgCopy)
        
def wait():
    cv2.waitKey(0)
    if(len(pointsX) == 2): cv2.destroyAllWindows()
    else:
        print("add more points")
        wait()

def math():
    #diffrent color space arrays
    #rgb
    b = []
    g = []
    r = []
    #hsv
    h = []
    s = []
    v = []
    #for graphing
    #rgb
    num_of_each_b = [0]*256
    num_of_each_g = [0]*256
    num_of_each_r = [0]*256
    #hsv
    num_of_each_h = [0]*180
    num_of_each_s = [0]*256
    num_of_each_v = [0]*256
    
    rgb_sv_x = []
    h_x = []
    
    rgb_stats = []
    hsv_stats = []

    for X in range(pointsX[0],pointsX[1]):
        for Y in range(pointsY[0],pointsY[1]):
            b.append(img[Y,X][0])
            g.append(img[Y,X][1])
            r.append(img[Y,X][2])
            num_of_each_b[b[-1]] += 1
            num_of_each_g[g[-1]] += 1
            num_of_each_r[r[-1]] += 1
            h.append(int(colorsys.rgb_to_hsv(r[-1]/255, g[-1]/255, b[-1]/255)[0] * 179))
            s.append(int(colorsys.rgb_to_hsv(r[-1]/255, g[-1]/255, b[-1]/255)[1] * 255))
            v.append(int(colorsys.rgb_to_hsv(r[-1]/255, g[-1]/255, b[-1]/255)[2] * 255))
            num_of_each_h[h[-1]] += 1
            num_of_each_s[s[-1]] += 1
            num_of_each_v[v[-1]] += 1
            
    for i in range(256):
        rgb_sv_x.append(i)
        if i < 180:
            h_x.append(i)
    
    rgb_stats.append([np.min(r),np.min(g),np.min(b)])
    rgb_stats.append([np.mean(r),np.mean(g),np.mean(b)])    
    rgb_stats.append([np.max(r),np.max(g),np.max(b)])
    rgb_stats.append([np.median(r),np.median(g),np.median(b)])
    
    hsv_stats.append([np.min(h),np.min(s),np.min(v)])
    hsv_stats.append([np.mean(h),np.mean(s),np.mean(v)])    
    hsv_stats.append([np.max(h),np.max(s),np.max(v)])
    hsv_stats.append([np.median(h),np.median(s),np.median(v)])
    
    print('##############')
    print('##RGB Values##')
    print('##############')
    print(f'Min: {rgb_stats[0]}')
    print(f'Mean: {rgb_stats[1]}')
    print(f'Max: {rgb_stats[2]}')
    print(f'Median: {rgb_stats[3]}')
    print('##############')
    print('##HSV Values##')
    print('##############')    
    print(f'Min: {hsv_stats[0]}')
    print(f'Mean: {hsv_stats[1]}')
    print(f'Max: {hsv_stats[2]}')
    print(f'Median: {hsv_stats[3]}')
    
    
    plt.plot(rgb_sv_x, num_of_each_r, color='red')
    plt.xlabel('amount of red')
    plt.ylabel('number of pixels')
    plt.title('red graph')
    plt.show()
    
    plt.plot(rgb_sv_x, num_of_each_g, color='green')
    plt.xlabel('amount of green')
    plt.ylabel('number of pixels')
    plt.title('green graph')
    plt.show()
    
    plt.plot(rgb_sv_x, num_of_each_b)
    plt.xlabel('amount of blue')
    plt.ylabel('number of pixels')
    plt.title('blue graph')
    plt.show()
    
    plt.plot(h_x, num_of_each_h, color='black')
    plt.xlabel('amount of hue')
    plt.ylabel('number of pixels')
    plt.title('hue graph')
    plt.show()
    
    plt.plot(rgb_sv_x, num_of_each_s, color='black')
    plt.xlabel('amount of saturation')
    plt.ylabel('number of pixels')
    plt.title('saturation graph')
    plt.show()
    
    plt.plot(rgb_sv_x, num_of_each_v, color='black')
    plt.xlabel('amount of value')
    plt.ylabel('number of pixels')
    plt.title('value graph')
    plt.show()

try:
    cv2.imshow('image',img)
except:
    raise Exception(f"{img_path}\{img_name} can't be read or dosen't exist or is an invalid file type or can't be shown")

cv2.setMouseCallback('image', mousePosition)    
wait()
math()

    