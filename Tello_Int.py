# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 15:11:37 2020

@author: dromp
"""

import Tello

t = Tello.Tello()

while True:
    cmd = input("Please enter command : ")
    if cmd == 'end': break
    try:
        response = t.send_command(cmd)
        print(response)
    except Exception as e:
        print(e)

t.close()
