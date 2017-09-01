import socket
import sys
from _thread import *
import json
import pygame

import numpy as np
import cv2
import base64


pygame.init()

clock = pygame.time.Clock()

pygame.joystick.init()

host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print('Waiting for a connection...')
def threaded_client(conn):
    
    while True:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        name = joystick.get_name()
        axes = joystick.get_numaxes() - 2
        
        axes_val = [0]*axes

        for i in range( axes ):
            axis = joystick.get_axis(i)
            axes_val[i] = round(axis*-1, 2)
        
        data_string = json.dumps(axes_val)
        conn.send(str.encode(data_string))
        
        data = conn.recv(50240)
        # Convert back to binary
        jpg_original = base64.b64decode(data)
        # Write to a file to show conversion worked
        np_array = np.fromstring(jpg_original, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        cv2.imshow("Cam", img)

        clock.tick(20)
        
    cv2.destroyAllWindows()
    conn.close()


while True:

    conn, addr = s.accept()
    print('Connected to: '+addr[0]+':'+str(addr[1]))

    start_new_thread(threaded_client,(conn,))

pygame.quit()