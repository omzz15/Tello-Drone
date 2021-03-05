# -*- coding: utf-8 -*-

import Tello
import sys

t = Tello.Tello()
command_file = 'commands.txt'
if len(sys.argv) > 1:
    command_file = sys.argv[1];

with open(command_file) as f:
    while True:
        cmd = f.readline().strip()
        if cmd == '': break
        print(cmd)
        try:
            response = t.send_command(cmd)
            print(response)
        except Exception as e:
            print(e)

t.close()
