# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:03:44 2020

@author: gauta
"""

import Tello
import time
import os
import cv2

show_original = True
movement_enabled = False;
cmd = ''


class MyTello(Tello.Tello):
    
    def __init__(self):
        self.ball_color_low = (60, 110, 20)
        self.ball_color_high = (125, 255, 160)
        #10, 170, 170
        #50, 255, 255
        self.bound_width_thres = 0.05
        self.bound_height_thres = 0.05
        self.ball_w = (0.1, 0.2)
        self.ball_h = (0.1, 0.2)
        self.ball_x = 0.15
        self.ball_y = 0.15
        self.directory = r'C:\development\projects\drone\Tello'
        #self.joy_stick_speed = 0.5
        self.max_move_frame_count = 30;
        self.cur_move_frame_count = 0;
        super().__init__()
        
    def draw_3x3_grid(self, img):
        vid_res = (img.shape[1], img.shape[0])
        img = cv2.line(img,(vid_res[0]//3,0),(vid_res[0]//3,vid_res[1]),(255,0,0),3)
        img = cv2.line(img,(2*(vid_res[0]//3),0),(2*(vid_res[0]//3),vid_res[1]),(255,0,0),3)
        img = cv2.line(img,(0,vid_res[1]//3),(vid_res[0],vid_res[1]//3),(255,0,0),3)
        img = cv2.line(img,(0,(2*vid_res[1]//3)),(vid_res[0],(2*vid_res[1]//3)),(255,0,0),3)
        return img
        
    def frame_pre_process(self, img):
        
        global cmd
        self.cur_move_frame_count += 1
        if(cmd == 's'):
            os.chdir(self.directory) 
            self.image_name = f'frame {self.cur_move_frame_count}.jpg'
            cv2.imwrite(self.image_name, img)
            time.sleep(.5)
            cmd = ''
        #if self.cur_move_frame_count > self.max_move_frame_count:
            #self.cur_move_frame_count -= 1
            
        global show_original
        global movement_enabled
        
        #blacking out background
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_img, self.ball_color_low, self.ball_color_high)
        res = cv2.bitwise_and(img,img, mask= mask)
        h, s, v = cv2.split(res)
        ret, thresh = cv2.threshold(v, 2, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        new_img = res
        if show_original: new_img = img
        if len(contours) == 0: return new_img
        new_img = self.draw_3x3_grid(new_img)
        # find the biggest countour (c) by the area
        mc = max(contours, key = cv2.contourArea)
        
        x,y,w,h = cv2.boundingRect(mc)
        vid_res = (img.shape[1], img.shape[0])
        if w > vid_res[0]*self.bound_width_thres and h > vid_res[1]*self.bound_height_thres:
            if movement_enabled:
                self.moveDrone(new_img, x,y,w,h)
            return cv2.rectangle(new_img,(x,y),(x+w,y+h),(0,255,0),2)
        else:
            self.joystick([0, 0, 0, 0])
            return new_img
    
    def moveDrone(self, img, x,y,w,h):
        vid_x, vid_y = img.shape[1], img.shape[0]
        x_diff = vid_x//2 - (x + w//2)
        y_diff = vid_y//2 - (y + h//2)
        z_diff = ((w*h) ** 0.5)/((vid_x*vid_y) ** 0.5)
        j_params = [0, 0, 0, 0]
        #forward and back
        if z_diff < 0.2 and z_diff > 0:
            j_params[1] = int(100 * (0.25 - z_diff)) + 3
        elif z_diff > 0.3:
            j_params[1] = int(70 * (0.25 - z_diff)) - 3

        if abs(x_diff) > self.ball_x*vid_x:
            j_params[0] = int(-0.04*x_diff)
            if x_diff < 0:
                j_params[0] += 3
            else:
                j_params[0] -= 3

        if abs(y_diff) > self.ball_y*vid_y:
            j_params[2] = int(0.095*y_diff)
            if y_diff < 0:
                j_params[2] -= 3
            else:
                j_params[2] += 5
        #if j_params[0] != 0 or j_params[1] != 0 or j_params[2] != 0:
        self.joystick(j_params)
        #self.cur_move_frame_count = 30

                
t = MyTello()
if movement_enabled: t.send_command("takeoff")
t.start_stream()
while t.running:
    cmd = input("Please enter 'end' to terminate : ")
    if cmd == 'end': break
    if cmd == 'n': show_original = True
    if cmd == 'm': show_original = False

t.close()
